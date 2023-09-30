from base.settings import Settings


class ApiSettings(Settings):
    mission_queue: str = "southbound.layer_1_aspirant"
    amqp_host_name: str = "rabbitmq"
    amqp_username: str = "rabbit"
    amqp_password: str = "carrot"

settings = ApiSettings(role_name = "ace-api")
