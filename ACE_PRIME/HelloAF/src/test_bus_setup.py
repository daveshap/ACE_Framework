import os
import asyncio
from ace.config import ConfigParser
from ace.settings import Settings
from ace import util
from ace.amqp.connection import AMQPConnectionManager
from ace.amqp.setup import AMQPSetupManager

settings = Settings(
    name="test",
    label="Test",
)

file_directory = util.get_file_directory()
config_path = os.path.join(file_directory, "ace", "bus_config.yaml")


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
    setup = AMQPSetupManager(settings, resources_config, exchanges_config, queues_config, bindings_config)
    channel = await connection.channel()  # Create a channel

    # Ensure the setup order is correct: exchanges, queues, bindings, pathways
    await setup.setup_exchanges(channel)
    await setup.setup_queues(channel)
    await setup.setup_queue_bindings(channel)
    await setup.setup_resource_pathways(channel)

    # Step 4: Sleep for one minute
    await asyncio.sleep(6)

    # Step 5: Call all the teardown methods in the proper order
    # Ensure the teardown order is correct: pathways, bindings, queues, then exchanges
    await setup.teardown_resource_pathways(channel)
    await setup.teardown_queue_bindings(channel)
    await setup.teardown_queues(channel)
    await setup.teardown_exchanges(channel)

    # Close the channel and connection
    await channel.close()
    await connection.close()

asyncio.run(test_setup_and_teardown())
