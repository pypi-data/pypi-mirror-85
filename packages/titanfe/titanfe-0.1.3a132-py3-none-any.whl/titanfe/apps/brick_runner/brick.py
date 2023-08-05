#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

""" A Brick within the brick runner """
import asyncio
import time

import janus

from titanfe import log as logging
from titanfe.apps.control_peer.brick import BrickInstanceDefinition
from titanfe.brick import InletBrickBase
from titanfe.utils import get_module, time_delta_in_ms, Flag
from .adapter import BrickAdapter, AdapterMeta
from ...constants import DEFAULT_PORT


class Brick:
    """Wraps all the Brick-Handling"""

    # pylint: disable=too-many-instance-attributes
    def __init__(self, instance_definition: BrickInstanceDefinition, metric_emitter, logger):
        self.metric_emitter = metric_emitter

        self.uid = instance_definition.uid
        self.name = instance_definition.name

        self.flow = instance_definition.flow

        self.exit_after_idle_seconds = (
            instance_definition.runtime_parameters.exit_after_idle_seconds
        )
        self.processing_parameters = instance_definition.processing_parameters

        self.default_port = next(iter(instance_definition.connections.output), DEFAULT_PORT)
        self.is_inlet = not instance_definition.connections.input
        self.is_outlet = not instance_definition.connections.output

        self.brick_type = instance_definition.base.name
        self.brick_family = instance_definition.base.family

        context = logging.FlowContext(*self.flow, self.uid, self.name)
        logging.global_context.update(context.asdict())

        self.log = logger.getChild("Brick")
        self.module = get_module(instance_definition.base.module_path)

        self.results = janus.Queue()
        self.adapter = BrickAdapter(
            AdapterMeta(brick=(self.uid, self.name), flow=(self.flow.uid, self.flow.name)),
            self.results.sync_q.put,
            self.log,
            self.default_port,
        )

        self.instance = None

        self.last_execution_start = None
        self.is_processing = Flag()

    def create_instance(self):
        """create an instance of the actual Brick"""
        try:
            self.instance = self.module.Brick(self.adapter, self.processing_parameters)
        except AttributeError:
            self.log.with_context.warning("Brick class is missing in module: %r", self.module)
            raise ImportError(f"Brick class is missing in module: {self.module}")

    def terminate(self):
        if isinstance(self.instance, InletBrickBase):
            self.instance.stop_processing()

    def __enter__(self):
        self.create_instance()
        self.instance.setup()

    def __exit__(self, exc_type, exc_val, exc_tb):
        self.instance.teardown()
        self.instance = None

    async def get_results(self):
        """async generator over the results from the brick"""
        queue = self.results.async_q

        while not (queue.closed and queue.empty()):
            packet, port = await queue.get()
            await self.metric_emitter.emit_packet_metrics(packet, self.execution_time)
            queue.task_done()
            yield packet, port

        raise StopAsyncIteration

    @property
    def execution_time(self):
        return time_delta_in_ms(self.last_execution_start)

    async def process(self, packet):
        with self.is_processing:
            await self.execute_brick(packet)

    async def execute_brick(self, packet):
        """run the brick module for the given packet in a separate thread"""
        self.log.info(
            "(%s) execute Brick: %s(%s) for %r", self.flow.name, self.name, self.uid, packet,
        )

        self.last_execution_start = time.time_ns()

        loop = asyncio.get_event_loop()
        result = await loop.run_in_executor(None, self.run_instance_processing, packet)

        if result is not None:
            port = self.default_port
            if not isinstance(result, tuple):
                packet.payload = result
            else:
                try:
                    packet.payload, port = result
                except ValueError:
                    raise ValueError("Invalid brick result ")
            self.log.debug("brick output: %r , port: %s" % (packet, port))
            await self.results.async_q.put((packet, port))

        await self.results.async_q.join()
        await self.metric_emitter.emit_brick_metrics(self.execution_time)
        if self.is_outlet:
            await self.metric_emitter.emit_packet_metrics(packet, self.execution_time)

    def run_instance_processing(self, packet):
        """do the actual execution of the brick module and return it's result"""
        try:
            return self.instance.process(packet.payload, packet.port)
        except Exception as error:  # pylint: disable=broad-except
            self.log.with_context.error("brick execution failed: %r", error, exc_info=True)
            return None
