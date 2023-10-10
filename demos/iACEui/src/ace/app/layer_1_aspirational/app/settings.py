from base.settings import Settings


settings = Settings(
    role_name="Aspirational Layer",
    control_bus_sub_queue="bus.control.L1",
    data_bus_pub_queue="bus.data.L1",
    control_bus_pub_queue="bus.control.L2",
    data_bus_sub_queue="bus.data.L2",
    debug = False,
)