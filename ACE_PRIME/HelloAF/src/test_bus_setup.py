import asyncio
from config import ConfigParser
from connection import AMQPConnectionManager
from setup import Setup
from ace.settings import Settings  # Assuming this is where your settings are defined

# Replace 'your_settings' with the actual settings object or values
settings = Settings(
    amqp_host_name='localhost',
    amqp_username='guest',
    amqp_password='guest',
    # ... other settings as needed
)

# Path to your YAML configuration file
config_path = 'bus_config.yaml'

async def test_setup_and_teardown():
    # Step 1: Load the YAML configuration
    config_parser = ConfigParser(config_path)
    resources_config = config_parser.get_resources()
    exchanges_config = config_parser.get_exchanges()
    queues_config = config_parser.get_queues()
    bindings_config = config_parser.get_bindings()

    # Step 2: Get an active connection to the RabbitMQ server
    connection_manager = AMQPConnectionManager(settings)
    connection = await connection_manager.get_connection()

    # Step 3: Feed the configuration to the Setup class and call all of the setup methods
    setup = Setup(settings, resources_config, exchanges_config, queues_config, bindings_config)
    channel = await connection.channel()  # Create a channel

    # Ensure the setup order is correct: exchanges, queues, then bindings
    await setup.setup_exchanges(channel)
    await setup.setup_queues(channel)
    await setup.setup_queue_bindings(channel)
    await setup.setup_resource_pathways(channel)

    # Step 4: Sleep for one minute
    await asyncio.sleep(60)

    # Step 5: Call all the teardown methods in the proper order
    # Ensure the teardown order is correct: bindings, queues, then exchanges
    await setup.teardown_queue_bindings(channel)
    await setup.teardown_queues(channel)
    await setup.teardown_exchanges(channel)

    # Close the channel and connection
    await channel.close()
    await connection.close()

# Run the test script
asyncio.run(test_setup_and_teardown())
