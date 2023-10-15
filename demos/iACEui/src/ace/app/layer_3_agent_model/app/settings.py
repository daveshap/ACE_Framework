from base.settings import Settings

settings = Settings(
    role_name="Agent Model Layer",
    control_bus_sub_queue="bus.control.L3",
    data_bus_pub_queue="bus.data.L3",
    control_bus_pub_queue="bus.control.L4",
    data_bus_sub_queue="bus.data.L4",
)