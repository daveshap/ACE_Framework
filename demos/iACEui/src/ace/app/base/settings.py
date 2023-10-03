from pydantic_settings import BaseSettings
from pydantic import PostgresDsn


class Settings(BaseSettings):
    role_name: str
    mode: str = 'OpenAI'
    model: str = 'gpt-3.5-turbo'
    # model: str = 'gpt-4'
    openai_api_key: str = 'put key in .env file'
    temperature: int = 0.0
    memory_max_tokens: int = 2000
    ai_retry_count: int = 3
    amqp_host_name: str = "rabbitmq"
    amqp_username: str = "rabbit"
    amqp_password: str = "carrot"
    logging_queue: str = "logging-queue"
    data_bus_sub_queue: str = "deadletter"
    control_bus_sub_queue: str = "deadletter"
    data_bus_pub_queue: str = "deadletter"
    control_bus_pub_queue: str = "deadletter"
    response_queue: str = "user-response-queue"

class DatabaseSettings(BaseSettings):
    database_uri: PostgresDsn = "postgresql://postgres:password@db:5432/ace-db"
