#!/usr/bin/env python3

import argparse

import docker
import yaml
import time
import subprocess

from ace.logger import Logger

logger = Logger(__name__)

DEFAULT_DOCKER_COMPOSE_FILE = 'docker-compose.yaml'
DEFAULT_MONITOR_SECONDS = 60


class ResourceManager():

    def __init__(self, args):
        self.args = args
        self.client = docker.from_env()
        self.services = self.get_services()
        self.containers = self.get_containers()

    def get_service_container(self, service_name):
        for container in self.client.containers.list(all=True):
            labels = container.labels
            if 'com.docker.compose.service' in labels and labels['com.docker.compose.service'] == service_name:
                return container
        return None

    def get_services(self):
        logger.debug(f"Loading docker-compose file: {self.args.compose_file}")
        with open(self.args.compose_file) as f:
            compose_config = yaml.safe_load(f)
        logger.debug(f"Extracting dependencies for services: {compose_config['services'].keys()}")
        services = {service: config.get('depends_on', []) for service, config in compose_config['services'].items()}
        return services

    def get_containers(self):
        logger.debug("Initializing Docker client")
        service_names = self.services.keys()
        logger.debug(f"Extracting container objects for services: {service_names}")
        containers = {service_name: self.get_service_container(service_name) for service_name in service_names}
        return containers

    def restart_with_deps(self, resource, restarted=None):
        restarted = restarted or set()
        if resource in restarted:
            logger.info(f"Resource {resource} already restarted, skipping")
            return
        logger.warning(f"Restarting resource {resource}...")
        self.containers[resource].restart()
        restarted.add(resource)
        if self.args.restart_deps:
            logger.info(f"Restarting dependencies of resource {resource}...")
            for service, deps in self.services.items():
                if resource in deps:
                    self.restart_with_deps(resource, restarted)

    def start_all_containers(self):
        try:
            logger.info("Starting containers")
            compose_args = [
                "docker",
                "compose",
                "up",
            ]
            if self.args.build:
                compose_args.append("--build")
            if self.args.detach:
                compose_args.append("--detach")
            subprocess.check_call(compose_args)
            logger.info("Containers started")
        except subprocess.CalledProcessError as e:
            logger.error(f"Docker Compose up command failed with error: {e}")
            raise

    def stop_all_containers(self):
        # Stop containers in reverse order.
        for resource in reversed(list(self.containers.keys())):
            logger.info(f"Stopping resource {resource}")
            self.containers[resource].stop()
        logger.info("All resources stopped")

    def monitor_containers(self):
        logger.info(f"Monitoring containers every {self.args.monitor_seconds} seconds")
        while True:
            time.sleep(self.args.monitor_seconds)
            logger.debug("Checking health of all resources")
            for resource, container in self.containers.items():
                # Refresh the container object
                container.reload()
                health = container.attrs['State']['Health']['Status']
                logger.debug(f"Resource {resource} health: {health}")
                if health != 'healthy':
                    self.restart_with_deps(resource)

    def wait_for_interrupt(self):
        while True:
            time.sleep(1)

    def run_with_monitor(self):
        self.start_all_containers()
        logger.info("Press CTRL-C to stop")
        if self.args.monitor_seconds:
            self.monitor_containers()
        else:
            self.wait_for_interrupt()

    def run(self):
        try:
            self.run_with_monitor()
        except KeyboardInterrupt:
            if self.args.detach:
                logger.info("Keyboard interrupt received, shutting down all resources...")
                self.stop_all_containers()


if __name__ == "__main__":

    parser = argparse.ArgumentParser(description='ACE Framework demo resource manager.')
    parser.add_argument('-b', '--build', action='store_true', help='Build the Docker containers')
    parser.add_argument('-d', '--detach', action='store_true', help='Run containers in the background')
    parser.add_argument('-r', '--restart-deps', action='store_true', help='Restart dependent containers on a container restart')
    parser.add_argument('-c', '--compose-file', default=DEFAULT_DOCKER_COMPOSE_FILE, help='Docker Compose file to use (default: %(default)s)')
    parser.add_argument('-m', '--monitor-seconds', default=DEFAULT_MONITOR_SECONDS, type=int, help='Number of seconds between monitor checks (default: %(default)s) -- set to 0 to disable')
    args = parser.parse_args()

    manager = ResourceManager(args)
    manager.run()
