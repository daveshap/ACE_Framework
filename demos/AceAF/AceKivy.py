from kivy.app import App
from kivy.uix.tabbedpanel import TabbedPanel
from kivy.uix.tabbedpanel import TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.boxlayout import BoxLayout
from kivy.clock import Clock

from ACE import ACE


class LayerOutput(BoxLayout):
    def __init__(self, layer_number, **kwargs):
        super().__init__(**kwargs)
        self.orientation = "vertical"
        self.layer_number = layer_number
        self.label = Label(text=f"Initializing Layer {self.layer_number}...")
        self.add_widget(self.label)

    def update_text(self, text):
        self.label.text = text


class ACEApp(App):

    def __init__(self, ace, **kwargs):
        super().__init__(**kwargs)
        self.ace = ace

    def build(self):
        self.tab_panel = TabbedPanel()
        self.layer_outputs = {}

        for layer_number in sorted(self.ace.layers.keys()):
            layer_output = LayerOutput(layer_number)
            tab = TabbedPanelItem(text=f"Layer {layer_number}")
            tab.add_widget(layer_output)
            self.tab_panel.add_widget(tab)

            # Store reference to LayerOutput for updating the UI
            self.layer_outputs[layer_number] = layer_output

        # Schedule ACE's run method to execute after the UI is set up
        Clock.schedule_once(self.start_ace, 1)

        return self.tab_panel

    def start_ace(self, *args):
        layer_outputs = self.ace.run()  # get layer outputs from ACE

        # Update the GUI using the layer_outputs.
        # For example, if you had a dictionary of TextInputs or Labels in self.layer_outputs_gui_elements:
        for layer_number, output in layer_outputs.items():
            self.layer_outputs_gui_elements[layer_number].text = output


if __name__ == '__main__':
    ace = ACE()
    ACEApp(ace).run()
