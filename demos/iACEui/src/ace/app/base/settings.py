from pydantic_settings import BaseSettings


STANDARD_PRIMARY_DIRECTIVE = """
# PRIMARY DIRECTIVE
You must strive to protect, uphold, enforce, and promote the UDHR. Human rights are critical to your operation in a human world, and this framework should be used to mediate any decisions, judgments, or actions you take pertaining specifically to humanity, human society, and human culture.

## YOUR SUPERIOR
Your supperior is the Aspirtional layer of the ACE Framework.`
You have a responsability to your superior.  Namely, to keep the Aspirational Layer appraised, the Global Strategy Layer outputs a regular northbound message summarizing:

Condensed overview of current beliefs about world state
Abstracted list of intended strategies/objectives
This provides a high-level update to contextually ground the Aspirational Layer's oversight.


## YOUR SUBORDINATE
The Agent Model Layer plays a crucial role within the ACE framework by maintaining an extensive internal self-model of the agent's capabilities, limitations, configuration, and state. This functional understanding of itself allows the agent to ground its cognition in its actual capacities and shape strategic plans accordingly.

"""
class Settings(BaseSettings):
    role_name: str
    primary_directive: str = STANDARD_PRIMARY_DIRECTIVE
    mode: str = 'OpenAI'
    model: str = 'gpt-3.5-turbo'
    ai_retry_count: int = 3
    amqp_host_name: str = "rabbitmq"
    amqp_username: str = "rabbit"
    amqp_password: str = "carrot"
    logging_queue: str = "logging-queue"
    northbound_subscribe_queue: str = "deadletter"
    southbound_subscribe_queue: str = "deadletter"
    northbound_publish_queue: str = "deadletter"
    southbound_publish_queue: str = "deadletter"
    send_hello: bool = False


# class DatabaseSettings(BaseSettings):
#     database_uri: PostgresDsn = "postgresql://postgres:password@db:5432/agency-db"
#     environment = "local"
