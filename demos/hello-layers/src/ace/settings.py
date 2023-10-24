import os
from typing import List
from pydantic_settings import BaseSettings

from ace import constants


class Settings(BaseSettings):
    name: str
    label: str
    amqp_host_name: str = os.getenv('ACE_RABBITMQ_HOSTNAME') or constants.DEFAULT_RABBITMQ_HOSTNAME
    amqp_username: str = os.getenv('ACE_RABBITMQ_USERNAME') or constants.DEFAULT_RABBITMQ_USERNAME
    amqp_password: str = os.getenv('ACE_RABBITMQ_PASSWORD') or constants.DEFAULT_RABBITMQ_PASSWORD
    logging_queue: str = "logging-queue"
    resource_log_queue: str = "resource-log-queue"
    log_dir: str = "/var/log/ace"
    system_integrity_queue: str = "system-integrity-queue"
    system_integrity_data_queue: str = "system-integrity-data-queue"
    debug_data_queue: str = "debug-data-queue"
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
    other_resources: List[str] = [
        'debug',
        'telemetry_manager',
        'logging',
        'busses',
    ]
