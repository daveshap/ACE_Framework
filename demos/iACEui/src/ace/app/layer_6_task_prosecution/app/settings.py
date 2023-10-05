from base.settings import Settings


settings = Settings(
    role_name="Task Prosecution Layer",
    control_bus_sub_queue="bus.control.L6",
    data_bus_pub_queue="bus.data.L6",
    control_bus_pub_queue="bus.control.none",
    data_bus_sub_queue="bus.data.none",
)
