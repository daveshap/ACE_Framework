from base.settings import Settings


settings = Settings(
    role_name="Cognitive Control Layer",
    control_bus_sub_queue="bus.control.L5",
    data_bus_pub_queue="bus.data.L5",
    control_bus_pub_queue="bus.control.L6",
    data_bus_sub_queue="bus.data.L6",
)
