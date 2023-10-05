import logging

from ace.framework.layer import Layer, LayerSettings

logging.basicConfig(level=logging.DEBUG)
logger = logging.getLogger(__name__)

# TODO: Add
PRIMARY_DIRECTIVE = ""


class Layer1(Layer):

    @property
    def settings(self):
        return LayerSettings(
            name="layer_1",
            label="Aspirational",
            primary_directive=PRIMARY_DIRECTIVE
        )

    # TODO: Add valid status checks.
    def status(self):
        logger.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)
