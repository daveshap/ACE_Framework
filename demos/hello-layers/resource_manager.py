import docker
import yaml
import time
import logging
import signal


def main():
    # Logging setup.
    logging.basicConfig(level=logging.DEBUG)
    logger = logging.getLogger('manage_containers')

    # Load dependencies.
    with open('config.yaml') as f:
        deps = yaml.safe_load(f)
    # Initialize Docker client.
    client = docker.from_env()

    # Start containers based on dependencies.
    containers = {}
    for resource, config in deps['ace_framework'].items():
        # Start dependencies first using docker-py.
        containers[resource] = client.containers.run(f"{resource}:latest",
                                                     name=resource,
                                                     detach=True,
                                                     healthcheck={
                                                         "test": ["CMD", "/usr/local/bin/check_resource_health"],
                                                         "interval": 5000000000,
                                                         "timeout": 3000000000,
                                                         "start_period": 0,
                                                         "retries": 3
                                                     })
        logger.info(f"Resource {resource} started")

    def restart_with_deps(resource, restarted=None):
        restarted = restarted or set()
        if resource in restarted:
            logger.info(f"Resource {resource} already restarted, skipping")
            return
        logger.warning(f"Restarting resource {resource} and its dependencies...")
        containers[resource].restart()
        restarted.add(resource)
        for dep, config in deps['ace_framework'].items():
            if resource in config['dependencies']:
                restart_with_deps(dep, restarted)

    try:
        while True:
            logger.debug("Checking health of all resources")
            for resource, container in containers.items():
                # Check container health.
                health = container.attrs['State']['Health']['Status']
                if health != 'healthy':
                    restart_with_deps(resource)
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
