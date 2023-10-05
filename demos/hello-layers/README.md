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
* Python >= 3.7

```sh
pip install -r requirements.txt
```

## Running the demo using the resource manager

From the root directory of the demo (where this README resides)

```sh
./resource_manager.py
```

## Running the demo in dev mode

From the root directory of the demo (where this README resides)

```sh
# Any additional args, such as --build, will be passed to docker compose
./dev.sh
```

This handles running `docker compose` with the appropriate config files for development, which shares the host `src` directory in the container, allowing for easy editing of the demo.

## Stopping the demo

Hit `Ctrl+c` or send a `SIGINT` to the running process.
