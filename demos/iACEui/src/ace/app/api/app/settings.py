from base.settings import Settings


class ApiSettings(Settings):
    mission_queue: str = "bus.control.L1"
    amqp_host_name: str = "rabbitmq"
    amqp_username: str = "rabbit"
    amqp_password: str = "carrot"

settings = ApiSettings(role_name = "ace-api")
