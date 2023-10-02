import logging

from ace.framework.layer import Layer, LayerSettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# TODO: Add
PRIMARY_DIRECTIVE = ""


class Layer6(Layer):

    @property
    def settings(self):
        return LayerSettings(
            name="layer_6",
            label="Task Prosecution",
            primary_directive=PRIMARY_DIRECTIVE
        )

    # TODO: Add valid status checks.
    def status(self):
        logger.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    def handle_message_control(self, data):
        pass

    def handle_message_data(self, data):
        pass
