#
# Copyright (c) 2019-present, wobe-systems GmbH
#
# Licensed under the Apache License, Version 2.0 (the "License");
# found in the LICENSE file in the root directory of this source tree.
#

"""Group represents multiple consumers of the same type"""

import asyncio
from asyncio import CancelledError
from collections import deque
from dataclasses import dataclass, field
from typing import List

from titanfe.utils import cancel_tasks, pairwise


@dataclass
class ConsumerGroupTasks:
    """Task of a Consumer group"""

    send_packets: asyncio.Task
    check_scaling: asyncio.Task
    handle_disconnects: field(default_factory=List)

    @property
    def all_tasks(self):
        return self.handle_disconnects + [self.send_packets, self.check_scaling]

    def __iter__(self):
        return iter(self.all_tasks)

    def add_disconnect_handler(self, on_disconnect: asyncio.coroutine):
        task = asyncio.create_task(on_disconnect)
        self.handle_disconnects.append(task)
        task.add_done_callback(self.handle_disconnects.remove)

    async def cancel(self):
        await cancel_tasks(self)


class ConsumerGroup:
    """Group consumers of same type and distribute packets between them"""

    slow_queue_alert_callback = lambda *args, **kwargs: None  # noqa

    def __init__(self, consumer_instance_id, queue, autoscale_queue_level=0):
        self.name = consumer_instance_id
        self.consumers = []
        self.packets = queue

        self.new_consumer_entered = asyncio.Event()
        self.autoscale_queue_level = autoscale_queue_level

        self.tasks = ConsumerGroupTasks(
            asyncio.create_task(self.send_packets()),
            asyncio.create_task(self.check_scaling_required(autoscale_queue_level)),
            [],
        )

    def __iter__(self):
        return iter(self.consumers)

    def __repr__(self):
        return f"Group(name={self.name}, consumers={self.consumers})"

    async def close(self):
        await asyncio.gather(*[consumer.close_connection() for consumer in self])
        await self.tasks.cancel()
        await self.packets.close()

    async def check_scaling_required(self, autoscale_queue_level=0, check_interval=0.2):
        """ watch the queue and dispatch an alert if it grows continuously,
            then wait for a new consumer before resetting the queue history - repeat."""

        try:
            if not autoscale_queue_level or not self.slow_queue_alert_callback:
                return

            while not self.consumers:
                await asyncio.sleep(0.1)
                if not self.packets.empty():
                    await self.slow_queue_alert_callback(self.name)
                    break

            # wait for the first consumer to come in
            await self.new_consumer_entered.wait()
            self.new_consumer_entered.clear()
            history = deque(maxlen=5)

            while True:
                await asyncio.sleep(check_interval)
                current_queue_size = self.packets.qsize()
                history.append(current_queue_size)

                if current_queue_size < autoscale_queue_level or len(history) < 3:
                    continue

                queue_is_growing = all(0 < prev <= curr for prev, curr in pairwise(history))
                if queue_is_growing:
                    await self.slow_queue_alert_callback(self.name)
                    await self.new_consumer_entered.wait()

                self.new_consumer_entered.clear()
                history.clear()
        except CancelledError:
            return

    def add(self, consumer):
        self.consumers.append(consumer)
        self.new_consumer_entered.set()
        self.tasks.add_disconnect_handler(self.handle_disconnect(consumer))

    async def handle_disconnect(self, consumer):
        await consumer.disconnected.wait()
        self.consumers.remove(consumer)
        if not self.consumers:
            await cancel_tasks([self.tasks.check_scaling])
            self.tasks.check_scaling = asyncio.create_task(
                self.check_scaling_required(self.autoscale_queue_level)
            )

    async def enqueue(self, packet):
        await self.packets.put(packet)

    async def send_packets(self):
        """send packets"""
        await self.new_consumer_entered.wait()
        while True:
            packet = await self.packets.get()
            consumer = await self.get_receptive_consumer()
            await consumer.send(packet)
            self.packets.task_done()

    async def get_receptive_consumer(self):
        """wait until any of the consumers is ready to receive and then return it"""
        while not self.consumers:
            await self.new_consumer_entered.wait()

        while self.consumers:
            done, pending = await asyncio.wait(
                {consumer.is_receptive() for consumer in self}, return_when=asyncio.FIRST_COMPLETED,
            )
            await cancel_tasks(pending)
            return done.pop().result()

    @property
    def has_unfinished_business(self):
        return self.packets.unfinished_tasks
