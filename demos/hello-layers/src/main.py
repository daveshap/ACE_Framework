import os
import time
import importlib
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(level=logging.DEBUG)


def loader(resource_name):
    try:
        resource_class_name = ''.join(word.title() for word in resource_name.split('_'))
        logger.debug(f"Converted resource_name to resource_class: {resource_class_name}")
        module = importlib.import_module(f'ace.framework.resource.{resource_name}')
        resource_class = getattr(module, resource_class_name)
        logger.debug(f"Imported {resource_class_name} from ace.framework.resource.{resource_name}")
        resource = resource_class()
        logger.debug(f"Created an instance of {resource_class}")
        logger.info(f"Calling start_resource method on the {resource_class} instance")
        resource.start_resource()
        logger.debug(f"Called start_resource method on the {resource_class} instance")
        return True
    except ImportError:
        logger.error(f"Failed to import module ace.framework.resource.{resource_name}", exc_info=True)
    except AttributeError:
        logger.error(f"Failed to get class {resource_class} from module ace.framework.resource.{resource_name}", exc_info=True)
    except Exception as e:
        logger.error(f"An error occurred: {e}", exc_info=True)


def main():
    ace_resource_name = os.getenv('ACE_RESOURCE_NAME')
    logger.info(f"Starting ACE resource: {ace_resource_name}")
    result = loader(ace_resource_name)
    while result:
        time.sleep(1000)


if __name__ == '__main__':
    main()
