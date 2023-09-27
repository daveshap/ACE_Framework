from base.settings import Settings


settings = Settings(
    role_name="layer_1_aspirant",
    northbound_subscribe_queue="northbound.layer_1_aspirant",
    southbound_subscribe_queue="southbound.layer_1_aspirant",
    southbound_publish_queue="southbound.layer_2_strategist",
    northbound_publish_queue="deadletter",
    send_hello=False,
)

prompts = {
    "prompt1": "something something {{input_string}}",
    "summarize_prompt": "something to summarize {{input_string}}",
}