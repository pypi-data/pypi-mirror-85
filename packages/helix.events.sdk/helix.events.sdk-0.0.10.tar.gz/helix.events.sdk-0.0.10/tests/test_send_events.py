from logging import getLogger, StreamHandler, INFO, Formatter, Logger
import socket
from sys import stdout
from time import sleep

from helix_events_sdk.event_reader import KafkaEventReader
from helix_events_sdk.event_writer import KafkaEventWriter
from helix_events_sdk.events.audit import AuditEvent
from helix_events_sdk.schemas.audit import Audit
from helix_events_sdk.schemas.audit_enums import AuditAction, AuditActionType, ResourceType
from helix_events_sdk.schemas.source import Source


def test_can_send_event(caplog) -> None:  # type: ignore
    caplog.set_level(INFO)
    event = AuditEvent(
        Source.BWELLBACKEND,
        Audit(
            patient_id="1",
            user_id="1",
            user_role="Patient",
            ip_address="192.168.1.1",
            client_slug="bwell",
            action=AuditAction.READ,
            action_type=AuditActionType.VIEW,
            accessed_resource=ResourceType.DIAGNOSES
        )
    )

    kafka_host = "localhost"
    kafka_port = "9092"
    audit_topic = "audit"
    wait_for_kafka(kafka_host, kafka_port)
    with KafkaEventWriter(
        get_logger(), kafka_host=kafka_host, kafka_port=kafka_port
    ) as kafka_event_writer:
        kafka_event_writer.write_event(event=event)

    with KafkaEventReader(
        topic=audit_topic,
        group_id='my-group',
        logger=get_logger(),
        kafka_host=kafka_host,
        kafka_port=kafka_port
    ) as kafka_event_consumer:
        audit_event = kafka_event_consumer.read_next_event()
        assert audit_event._attributes['id'] == event._attributes['id']
        assert audit_event.data == event.data


def get_logger() -> Logger:
    logger = getLogger(__name__)
    stream_handler: StreamHandler = StreamHandler(stdout)
    stream_handler.setLevel(level=INFO)
    # noinspection SpellCheckingInspection
    formatter: Formatter = Formatter(
        '%(asctime)s.%(msecs)03d %(levelname)s %(module)s %(lineno)d - %(funcName)s: %(message)s'
    )
    stream_handler.setFormatter(formatter)
    logger.addHandler(stream_handler)
    return logger


def wait_for_kafka(host: str, port: str) -> None:
    a_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    location = (host, int(port))
    result_of_check = 1
    while result_of_check != 0:
        result_of_check = a_socket.connect_ex(location)
        sleep(5)
