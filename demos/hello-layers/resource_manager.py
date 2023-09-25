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
    for resource, config in deps['ace_framework'].items():
        # Start dependencies first using docker-py.
        depends_on = {dep: {'condition': 'service_started'} for dep in config['dependencies']}
        client.containers.run(f"{resource}:latest",
                              name=resource,
                              detach=True,
                              healthcheck={
                                  "test": ["CMD", "layer_status"],
                                  "interval": 5,
                                  "timeout": 3,
                                  "retries": 3
                              },
                              depends_on=depends_on)
        logger.debug(f"{resource} started")

    try:
        while True:
            for container in client.containers.list():
                # Check container health.
                health = container.healthcheck.get('Status')
                if health != 'Up':
                    logger.warning(f"{container.name} health check failed, restarting...")
                    container.restart()

                else:
                    logger.debug(f"{container.name} health check succeeded")
            time.sleep(5)

    except KeyboardInterrupt:
        logger.info("Keyboard interrupt received, shutting down...")
        # Stop containers in reverse order.
        for container in reversed(client.containers.list()):
            logger.info(f"Stopping {container.name}")
            container.stop()
        logger.info("All resources stopped")


if __name__ == "__main__":
    # Register signal handler for Ctrl+C
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    main()
