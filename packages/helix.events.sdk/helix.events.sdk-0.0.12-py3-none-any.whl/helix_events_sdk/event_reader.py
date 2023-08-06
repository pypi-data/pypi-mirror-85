import os
from logging import Logger
from typing import Optional, Any

from cloudevents.http import CloudEvent, from_json
from kafka import KafkaConsumer


class BaseEventReader:
    def __init__(self, logger: Logger):
        self._logger = logger

    def read_next_event(self) -> CloudEvent:
        pass


class KafkaEventReader(BaseEventReader):
    def __enter__(self) -> BaseEventReader:
        return self

    def __exit__(self, exc_type: Any, exc_val: Any, exc_tb: Any) -> None:
        self._consumer.close()

    def __init__(
        self,
        logger: Logger,
        topic: str,
        group_id: str,
        kafka_host: Optional[str] = None,
        kafka_port: Optional[str] = None
    ):
        if not kafka_host:
            kafka_host = os.getenv('KAFKA_HOST')

        if not kafka_port:
            kafka_port = os.getenv('KAFKA_PORT')

        assert kafka_host
        assert kafka_port
        self._consumer = KafkaConsumer(
            topic,
            bootstrap_servers=[f'{kafka_host}:{kafka_port}'],
            group_id=group_id,
            consumer_timeout_ms=30000,
            auto_offset_reset='earliest',
            enable_auto_commit=True
        )
        super().__init__(logger)

    def read_next_event(self) -> CloudEvent:
        self._logger.info('waiting for messages')
        returned_event = next(self._consumer).value
        return from_json(returned_event)
