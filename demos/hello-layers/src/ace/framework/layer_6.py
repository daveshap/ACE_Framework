from ace.framework.layer import Layer, LayerSettings

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
