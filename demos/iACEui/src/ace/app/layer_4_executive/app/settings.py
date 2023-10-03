from base.settings import Settings


settings = Settings(
    role_name="Executive Layer",
    control_bus_sub_queue="bus.control.L4",
    data_bus_pub_queue="bus.data.L4",
    control_bus_pub_queue="bus.control.L5",
    data_bus_sub_queue="bus.data.L5",
)
