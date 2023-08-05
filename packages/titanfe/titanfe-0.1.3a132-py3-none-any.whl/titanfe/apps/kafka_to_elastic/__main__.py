"""
kafka_to_elastic

Usage:
  kafka_to_elastic [-k <bootstrap_servers>] [-e <elastic_host>] [<topic> [<topic> ...]]
  kafka_to_elastic (-h | --help)

Example:
  kafka_to_elastic --kafka=127.0.0.1:9092 --elastic=127.0.0.1 a_topic another_topic

Topics:
  pass one or more topics as positional arguments [default: titanfe.metrics]

Options:
  -h, --help     Show this screen.

  -k <bootstrap_servers>, --kafka=<bootstrap_servers>
      the Kafka bootstrap_servers to connect to as `<host>:<port> <host:port> ...`
      [default: 10.14.0.23:9092]

  -e <elastic_host>, --elastic=<elastic_host>
      the elastic host `<hostname_or_ip>` [default: 10.14.0.21]
"""

# pylint: disable=broad-except, missing-docstring
# missing-function-docstring, missing-class-docstring

import os
import asyncio
import pickle
import signal
from contextlib import suppress
from datetime import datetime

import docopt
from aiokafka import AIOKafkaConsumer, ConsumerStoppedError
from elasticsearch import AsyncElasticsearch
from elasticsearch.helpers import async_bulk


async def main():
    args = docopt.docopt(__doc__)

    signals = signal.SIGINT, signal.SIGTERM

    if os.name != "nt":  # not available on windows
        signals += (signal.SIGHUP,)  # pylint: disable=no-member

    for sign in signals:
        signal.signal(sign, schedule_shutdown)

    bootstrap_servers = args["--kafka"]
    elastic_host = args["--elastic"]
    topics = args["<topic>"] or ["titanfe.metrics"]

    print("Reading", topics, "From", bootstrap_servers, "To", elastic_host)

    async with KafkaReader(topics, bootstrap_servers=bootstrap_servers) as kafka, ElasticWriter(
        elastic_host=elastic_host
    ) as elastic:  # pylint: disable= ; noqa
        async for topic, records in kafka.read():
            len_records = f"{len(records)} record{'s' if len(records) > 1 else ''}"
            print(f"processing {len_records} from {topic.topic}")
            msgs = list(transform_kafka_to_elastic(records))
            await elastic.bulk_insert(msgs)


def schedule_shutdown(sign, _):
    print(f"Received {signal.Signals(sign).name} ...")  # pylint: disable=no-member

    async def shutdown():
        tasks = [t for t in asyncio.all_tasks() if t is not asyncio.current_task()]
        for task in tasks:
            task.cancel()

        print(f"Cancelling outstanding tasks ({len(tasks)})")
        await asyncio.gather(*tasks)

    asyncio.create_task(shutdown())


class KafkaReader:
    def __init__(self, topics, bootstrap_servers):
        self.consumer = AIOKafkaConsumer(
            *topics,
            loop=asyncio.get_event_loop(),
            bootstrap_servers=bootstrap_servers,
            # auto_offset_reset='earliest',
        )

    async def start(self):
        await self.consumer.start()

    async def stop(self):
        await self.consumer.stop()

    async def __aenter__(self):
        await self.start()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.stop()

    def __aiter__(self):
        return self

    async def __anext__(self):
        while True:
            try:
                batch = await self.consumer.getmany(timeout_ms=1000)
            except (asyncio.CancelledError, ConsumerStoppedError):
                raise StopAsyncIteration

            if not batch:
                print(".", end="", flush=True)
                continue

            return batch

    async def read(self):
        async for batch in self:
            for topic, records in batch.items():
                yield topic, records


class ElasticWriter:
    def __init__(self, elastic_host):
        self.elastic = AsyncElasticsearch(hosts=[{"host": elastic_host}])

    async def __aenter__(self):
        await self.elastic.__aenter__()
        return self

    async def __aexit__(self, exc_type, exc_val, exc_tb):
        await self.elastic.close()

    async def bulk_insert(self, document_generator):
        await async_bulk(self.elastic, document_generator)


def transform_kafka_to_elastic(batch):
    def transform(message):
        content = pickle.loads(message.value)
        content["@timestamp"] = content.pop("timestamp")

        doc_type = content["content_type"]
        index = f"{doc_type}-{datetime.now():%Y-%m-%d}"

        return {
            "_op_type": "index",
            "_index": index,
            "_type": doc_type,
            "_source": content,
        }

    for message in batch:
        try:
            yield transform(message)
        except Exception as error:
            print("Failed to transform", message, error)


if __name__ == "__main__":

    async def run_main():
        try:
            with suppress(asyncio.CancelledError):
                await main()
        except Exception as error:
            print("Error:", repr(error))

    asyncio.run(run_main())
