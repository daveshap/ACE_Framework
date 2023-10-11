from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    name: str
    label: str
    amqp_host_name: str = "rabbitmq"
    amqp_username: str = "rabbit"
    amqp_password: str = "carrot"
    logging_queue: str = "logging-queue"
    log_dir: str = "/var/log/ace"
    system_integrity_queue: str = "system-integrity-queue"
    system_integrity_data_queue: str = "system-integrity-data-queue"
    telemetry_subscribe_queue: str = "telemetry-subscribe-queue"
    telemetry_subscriptions: List[str] = []
    layers: List[str] = [
        'layer_1',
        'layer_2',
        'layer_3',
        'layer_4',
        'layer_5',
        'layer_6',
    ]
