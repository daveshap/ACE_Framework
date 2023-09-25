# "Hello, Layers!" Demo

## Objective

A right of passage when learning any new software framework (and a simple first step to ensure its basic systems are operating correctly) is the ubiquitous "Hello, World!" demo.

In the same spirit, "Hello, Layers!" is the ACE Framework's most basic demo. If you run this and it outputs "Hello, Layers!", you just ran a bare bones ACE :)

## What happens under the hood

1. A resource manager script starts up all aspects of the ACE
   * Each aspect is a `resource`, one resource per container
   * Resource depedencies of the ACE are declared in `config.yaml`
   * Resources are started from the top down, and shut down from the bottom up
   * The resource manager periodically monitors the 'health' of every resource, and if it failed, restarts the resource and any dependencies
2. Once all resources are up, a simple communication exchange of test messages ensures all layers are communicating along the busses
3. With the communication test checks complete, the ACE fullfills its mission by outputting "Hello, Layers!" to the console
4. Ooohs and ahhhs ensue :P

## Setup

### Requirements

* Docker
* Python >= 3.7

```
pip install -r requirements.txt
```

## Running the demo

```
python resource_manager.py
```

## Stopping the demo

Hit `Ctrl+c` or send a `SIGINT` to the running process.
