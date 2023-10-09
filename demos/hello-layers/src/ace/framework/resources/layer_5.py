from ace.framework.layer import Layer, LayerSettings
from ace.framework.prompts.identities import l5_identity

class Layer5(Layer):

    @property
    def settings(self):
        return LayerSettings(
            name="layer_5",
            label="Cognitive Control",
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    def set_identity(self):
        self.identity=l5_identity

    def process_layer_messages(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        pass