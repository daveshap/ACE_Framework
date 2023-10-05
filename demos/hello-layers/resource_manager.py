#!/usr/bin/env python3

import argparse

import docker
import yaml
import time
import subprocess

from ace.logger import Logger

logger = Logger(__name__)

DOCKER_COMPOSE_FILE = 'docker-compose.yaml'


def get_service_container(client, service_name):
    for container in client.containers.list(all=True):
        labels = container.labels
        if 'com.docker.compose.service' in labels and labels['com.docker.compose.service'] == service_name:
            return container
    return None


def get_services():
    logger.debug(f"Loading docker-compose file: {DOCKER_COMPOSE_FILE}")
    with open(DOCKER_COMPOSE_FILE) as f:
        compose_config = yaml.safe_load(f)
    logger.debug(f"Extracting dependencies for services: {compose_config['services'].keys()}")
    services = {service: config.get('depends_on', []) for service, config in compose_config['services'].items()}
    return services


def get_containers(services):
    logger.debug("Initializing Docker client")
    client = docker.from_env()
    logger.debug(f"Extracting container objects for services: {services.keys()}")
    containers = {service: get_service_container(client, service) for service in services.keys()}
    return containers


def restart_with_deps(services, containers, resource, restarted=None):
    restarted = restarted or set()
    if resource in restarted:
        logger.info(f"Resource {resource} already restarted, skipping")
        return
    logger.warning(f"Restarting resource {resource} and its dependencies...")
    # TODO: Fix.
    return
    containers[resource].restart()
    restarted.add(resource)
    for service, deps in services.items():
        if resource in deps:
            restart_with_deps(services, containers, resource, restarted)


def start_all_containers():
    try:
        logger.info("Starting containers")
        # subprocess.check_call(["docker", "compose", "up", "--build", "-d"])
        subprocess.check_call(["docker", "compose", "up"])
        logger.info("Containers started")
    except subprocess.CalledProcessError as e:
        logger.error(f"Docker Compose up command failed with error: {e}")
        raise


def stop_all_containers(containers):
    # Stop containers in reverse order.
    for resource in reversed(list(containers.keys())):
        logger.info(f"Stopping resource {resource}")
        containers[resource].stop()
    logger.info("All resources stopped")


def monitor_containers(services, containers):
    while True:
        logger.debug("Checking health of all resources")
        for resource, container in containers.items():
            # Check container health.
            health = container.attrs['State']['Health']['Status']
            logger.debug(f"Resource {resource} health: {health}")
            if health != 'healthy':
                restart_with_deps(services, containers, resource)
        time.sleep(5)


def main():
    start_all_containers()
    services = get_services()
    containers = get_containers(services)
    try:
        monitor_containers(services, containers)
    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down all resources...")
        stop_all_containers(containers)


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='ACE Framework demo resource manager.')
    parser.add_argument('-b', '--build', action='store_true', help='Build the Docker containers')
    parser.add_argument('-d', '--detach', action='store_true', help='Run containers in the background')
    parser.add_argument('-r', '--restart-deps', action='store_true', help='Restart dependent containers on a container restart')
    args = parser.parse_args()
    main()
