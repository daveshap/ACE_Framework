# ACE AMQP configuration/setup

## File structure

This directory contains the code that handles the configuration of the ACE messaging system (busses, etc.) and setup of the accoompanying RabbitMQ exchanges/queues/bindings.

### `messaging_config.yaml`

This file contains the full configuration for the **static** AMQP configuration (those settings that rarely if ever change).

It is well-commented and should contain enough documentation to understand how to make adjustments to the static configuration.

### `config_parser.py`

By default, parses `messaging_config.yaml` into a `ConfigParser` instance.

### `connection.py`

Manages the connection with the RabbitMQ server based on the passed `Settings` instance.

### `setup.py`

Transforms the passed `ConfigParser` instance into RabbitMQ exchanges/queues/bindings.

Can also be used by other code to dynamically create exchanges/queues/bindings.

### `test_bus_setup.py`

Run a complete test of the setup. This does the following:

1. Creates all RabbitMQ exchanges/queues/bindings
2. Waits for the user to hit enter
3. Tears down all RabbitMQ exchanges/queues/bindings

## Testing the setup

1. Install Docker and Docker Compose in a non-root configuration.
2. Create the docker containers for the test:
   ```sh
   ACE_LOG_LEVEL=DEBUG docker compose -f docker-compose-amqp-test.yaml up
    ```
3. Log into the test container:
   ```sh
   docker exec -it helloaf-test-1 bash
   ```
4. Run the test:
   ```sh
   python ace/amqp/test_bus_setup.py
   ```

To see the final RabbitMQ configuration, you can log into the RabbitMQ UI at `http://localhost:15672` -- the username and password are available in `docker-compose.yaml` in the root directory of the demo.
