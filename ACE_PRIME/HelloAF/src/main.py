import os
import time
import importlib

from ace import util
from ace.logger import Logger

logger = Logger(os.path.basename(__file__))

RESOURCE_LOADER_DIRECTORIES = [
    "custom",
    "core",
]


def load_resource(resource_class_name, import_path):
    try:
        module = importlib.import_module(import_path)
    except ImportError:
        logger.debug(
            f"No import available for module {import_path}",
        )
        return
    try:
        resource_class = getattr(module, resource_class_name)
        return resource_class
    except AttributeError:
        logger.error(
            f"Failed to get class {resource_class} from module {import_path}",
            exc_info=True,
        )


def loader(resource_name):
    try:
        resource_class_name = util.snake_to_class(resource_name)
        logger.debug(
            f"Converted resource_name to resource_class: {resource_class_name}"
        )
        subdirectory = os.environ.get("ACE_RESOURCE_SUBDIRECTORY", "hello_layers")
        logger.debug(f"ACE_RESOURCE_SUBDIRECTORY: {subdirectory}")
        for directory in RESOURCE_LOADER_DIRECTORIES:
            import_path = f"ace.resources.{directory}.{subdirectory}.{resource_name}"
            resource_class = load_resource(
                resource_class_name, import_path
            )
            if resource_class:
                break
        if not resource_class:
            import_path = f"ace.framework.resources.{resource_name}"
            logger.debug(f"No custom resource found, importing from {import_path}")
            resource_class = load_resource(
                resource_class_name, import_path
            )
        if not resource_class:
            logger.error(
                f"No import available for resource {resource_name}",
            )
            return False
        logger.debug(
            f"Imported {resource_class_name} from {import_path}"
        )
        resource = resource_class()
        logger.debug(f"Created an instance of {resource_class}")
        logger.info(f"Calling start_resource method on the {resource_class} instance")
        resource.start_resource()
        logger.debug(f"Called start_resource method on the {resource_class} instance")
        return True
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)


def main():
    ace_resource_name = os.getenv("ACE_RESOURCE_NAME")
    logger.info(f"Starting ACE resource: {ace_resource_name}")
    result = loader(ace_resource_name)
    while result:
        time.sleep(1000)


if __name__ == "__main__":
    main()
