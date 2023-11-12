# "Hello, Layers!" Demo

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
3. With the communication test checks complete, the ACE attempts to fullfill its mission:
   * This is accomplished by fully exercising the agents at each layer of the ACE
   * The mission is simple: output "Hello, Layers!" to the console
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

You'll need to export the `OPENAI_API_KEY` environment variable on your system to a valid OpenAI API key, for example:

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
