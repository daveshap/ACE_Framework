from base.settings import Settings

settings = Settings(
    role_name="layer_2_strategist",
    send_hello=False,
    northbound_subscribe_queue="northbound.layer_2_strategist",
    southbound_subscribe_queue="southbound.layer_2_strategist",
    southbound_publish_queue="southbound.layer_3_agent",
    northbound_publish_queue="northbound.layer_1_aspirant",
)
