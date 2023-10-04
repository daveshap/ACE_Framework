import docker
import yaml
import time
import signal
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


def main():
    # Start containers based on dependencies.
    try:
        logger.info("Starting containers")
        subprocess.check_call(["docker", "compose", "up", "--build", "-d"])
        logger.info("Containers started")
    except subprocess.CalledProcessError as e:
        logger.error(f"Docker Compose up command failed with error: {e}")
        raise

    # Load docker-compose.yaml.
    logger.debug(f"Loading docker-compose file: {DOCKER_COMPOSE_FILE}")
    with open(DOCKER_COMPOSE_FILE) as f:
        compose_config = yaml.safe_load(f)
    # Extract dependencies.
    logger.debug(f"Extracting dependencies for services: {compose_config['services'].keys()}")
    services = {service: config.get('depends_on', []) for service, config in compose_config['services'].items()}

    # Initialize Docker client.
    logger.debug("Initializing Docker client")
    client = docker.from_env()

    # Get container objects for the services.
    logger.debug(f"Extracting container objects for services: {services.keys()}")
    containers = {service: get_service_container(client, service) for service in services.keys()}

    def restart_with_deps(resource, restarted=None):
        restarted = restarted or set()
        if resource in restarted:
            logger.info(f"Resource {resource} already restarted, skipping")
            return
        logger.warning(f"Restarting resource {resource} and its dependencies...")
        containers[resource].restart()
        restarted.add(resource)
        for service, deps in services.items():
            if resource in deps:
                restart_with_deps(service, restarted)

    try:
        while True:
            logger.debug("Checking health of all resources")
            # TODO: Re-enable this once resources run correctly.
            # for resource, container in containers.items():
            #     # Check container health.
            #     health = container.attrs['State']['Health']['Status']
            #     if health != 'healthy':
            #         restart_with_deps(resource)
            time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down all resources...")
        # Stop containers in reverse order.
        for resource in reversed(list(containers.keys())):
            logger.info(f"Stopping resource {resource}")
            containers[resource].stop()
        logger.info("All resources stopped")


if __name__ == "__main__":
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
