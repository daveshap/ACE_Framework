# "HelloAF" PRIME Demo

## Objective

A right of passage when learning any new software framework (and a simple first step to ensure its basic systems are operating correctly) is the ubiquitous "Hello, World!" demo.

In the same spirit, "Hello, Layers!" is the ACE Framework's most basic demo. If you run this and it outputs "Hello, Layers!", you just ran a bare bones ACE :)

## What happens under the hood

1. A resource manager script starts up all components of the ACE
   * Each component is a `resource`, one resource per Docker container
   * Resource depedencies of the ACE are inferred from `docker-compose.yaml`
   * Resources are started from the top down, and shut down from the bottom up
   * The resource manager periodically monitors the 'health' of every resource, restarting containers as necessary
2. Once all resources are up, a simple communication exchange of test messages ensures all layers are communicating along the busses (Power On Self-Test)
3. With the communication test checks complete, the ACE attempts to fullfill its mission
4. Ooohs and ahhhs ensue :P

## Setup

### Requirements

* Docker
* Docker Compose
* Python >= 3.7

The user running the demo will need permissions to execute `docker` commands (e.g.  Rootless mode).

*NOTE: This setup has only been tested from a shell environment, running it from other environments (such as IDEs) may not work.*

```sh
pip install -r requirements.txt
```

### Credentials

If you're using OpenAI models, you'll need to export the `OPENAI_API_KEY` environment variable on your system to a valid OpenAI API key, for example:

```sh
export OPENAI_API_KEY="your_openai_api_key_here"
```

RabbitMQ is configured by default with username `rabbit`, password `carrot`. You can log into the running RabbitMQ web console at `http://localhost:15672` once the system is started up.

You can also customize the RabbitMQ hostname/login credentials by exporting the following variables on your host:

```sh
export ACE_RABBITMQ_HOSTNAME="some_hostname"
export ACE_RABBITMQ_USERNAME="some_username"
export ACE_RABBITMQ_PASSWORD="some_password"
```

## Running the demo using the resource manager

From the root directory of the demo (where this README resides)

```sh
./resource_manager.py
```

## Running the demo in dev mode

If you plan on hacking the Python files in the demo, you'll want to run it in dev mode, which syncs the demo files on your host with the containers, allowing editing without rebuilding the containers.

From the root directory of the demo (where this README resides)

```sh
# Any additional args, such as --build, will be passed to docker compose
./dev.sh
```

This handles running `docker compose` with the appropriate config files for development, which shares the host `src` directory in the container, allowing for easy editing of the demo.

## Stopping the demo

Hit `Ctrl+c` or send a `SIGINT` to the running process.

## Logging

By default, third party libraries are set to log level `WARNING`, and the ACE logging is level `INFO`.

To adjust these, you can pass the following environment variables when running via either of the above methods:

```sh
ACE_THIRD_PARTY_LOG_LEVEL=DEBUG ACE_LOG_LEVEL=DEBUG ./dev.sh
```

The `logging` resource stores log messages, by default clearing old log messages at the start of a new run. You can log into the `logging` resource:

```sh
docker exec -it helloaf-logging-1 bash
```

By default, logs are stored in that resource at `/var/log/ace`.


## Debugging

There is a `debug` resource that allows you to connect to a running ACE via a simple text user interface. This allows you to:

1. Pause the ACE
2. View current messages on the bus at the time the ACE was paused
3. Edit bus messages
4. Submit bus messages for an individual layer into the ACE for that layer to execute

To use the debugger, log into the `debug` resource:
```sh
docker exec -it helloaf-debug-1 bash
```

Run the debugging interface:

```sh
python debug-ace-tui.py
```

Simple event logging and keyboard shortcuts are listed at the top.

## Building custom intelligence layers

A simple loading mechanism allows you to implement custom resources when starting up the ACE.

This allows you to benefit from the existing support features (containers, messaging framework, logging, debugging, telemetry support, etc.) while still implementing your own layer intelligence.

1. Create a directory under `resources/custom` -- the directory name must be a valid Python identifier, e.g. `example_ace`
2. Inside the directory, place one Python file for each layer
  * The filename must be the name of the layer resource, e.g. `layer_1` would be `layer_1.py`
  * The class name in the file must be the camel-cased version of the file name, e.g. `layer_1` becomes `Layer1`
  * The class must inherit from the base `Layer` class:
    ```python
    from ace.framework.layer import Layer
    class Layer1(Layer):
        # Layer logic
    ```
3. Start the ACE using the `dev.sh` script, passing the name of the created directory in the `ACE_RESOURCE_SUBDIRECTORY` environment variable:
   ```sh
   ACE_RESOURCE_SUBDIRECTORY=example_ace ACE_LOG_LEVEL=DEBUG ./dev.sh
   ```

For more information on how to implement the layers, examine the existing layer code under `resources/core`.
