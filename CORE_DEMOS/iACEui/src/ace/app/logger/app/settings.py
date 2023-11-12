from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    amqp_host_name: str = "rabbitmq"
    amqp_username: str = "rabbit"
    amqp_password: str = "carrot"
    logging_queue: str = "logging-queue"

settings = Settings()
