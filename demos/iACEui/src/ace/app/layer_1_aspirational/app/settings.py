from base.settings import Settings


settings = Settings(
    role_name="Aspirational Layer",
    northbound_subscribe_queue="northbound.layer_1_aspirant",
    southbound_subscribe_queue="southbound.layer_1_aspirant",
    southbound_publish_queue="southbound.layer_2_strategist",
    northbound_publish_queue="deadletter",
)