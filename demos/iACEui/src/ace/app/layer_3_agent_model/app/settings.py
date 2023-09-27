from base.settings import Settings

settings = Settings(
    role_name="layer_3_agent",
    send_hello=False,
    northbound_subscribe_queue="northbound.layer_3_agent",
    southbound_subscribe_queue="southbound.layer_3_agent",
    southbound_publish_queue="southbound.layer_4_executive",
    northbound_publish_queue="northbound.layer_2_strategist",
)
