from ace.framework.layer import Layer, LayerSettings

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
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)
