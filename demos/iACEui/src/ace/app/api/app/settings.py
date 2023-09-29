from base.settings import Settings


class ApiSettings(Settings):
    mission_queue: str = "southbound.layer_1_aspirant"

settings = ApiSettings(role_name = "ace-api")
