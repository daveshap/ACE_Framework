from kivy.app import App
from kivy.uix.boxlayout import BoxLayout
from kivy.uix.tabbedpanel import TabbedPanel, TabbedPanelItem
from kivy.uix.label import Label
from kivy.uix.textinput import TextInput
from kivy.uix.button import Button
from flask import Flask, request, jsonify
import threading
import requests
from kivy.lang import Builder
from kivy.uix.scrollview import ScrollView

app = Flask(__name__)

# Dynamic registration of Flask routes
# LAYER_NAMES = ["L0Console", "L1Aspirational", "L2Strategy", "L3Agent", "L4Executive", "L5Cognitive", "L6Prosecution"]


@app.route('/layer_update', methods=['POST'])
def layer_update():
    data = request.json
    layer_number = data.get('layer_number')
    message = data.get('message', '')

    # Check if layer_name is valid, if not, send an error response
    # if layer_name not in LAYER_NAMES:
    #     return jsonify({"status": "error", "message": "Invalid layer name"})

    # Convert layer_name to layer_number for update_label function
    # layer_number = LAYER_NAMES.index(layer_number)
    kivy_app.update_label(layer_number, message)
    return jsonify({"status": "received"})


def run_flask_app():
    app.run(port=5000)


class KivyApp(App):

    def __init__(self, **kwargs):
        super(KivyApp, self).__init__(**kwargs)
        # Initialize a list with empty strings for each layer's history
        # 7 items (0) for the console and (1-6) for layers 1 to 6
        self.history = [""] * 7

        # Initialize the ScrollViews and Labels for each layer
        self.views = []
        self.labels = []

    def build(self):
        self.main_layout = BoxLayout(orientation='vertical')
        self.tab_panel = TabbedPanel(do_default_tab=False)

        self.tab_console = TabbedPanelItem(text='Console')
        self.tab1 = TabbedPanelItem(text='L1 Aspirational')
        self.tab2 = TabbedPanelItem(text='L2 Strategy')
        self.tab3 = TabbedPanelItem(text='L3 Agent')
        self.tab4 = TabbedPanelItem(text='L4 Executive')
        self.tab5 = TabbedPanelItem(text='L5 Cognitive')
        self.tab6 = TabbedPanelItem(text='L6 Prosecution')

        for i in range(7):  # 7 layers including the Console
            self.history[i] = "Listening to Messages...\n"
            view = ScrollView()
            label = Label(text=self.history[i], size_hint_y=None)
            label.bind(texture_size=label.setter('size'))
            view.add_widget(label)

            self.views.append(view)
            self.labels.append(label)

        # Message histories
        # self.layer_history[0] = "Waiting for message on console...\n"
        # self.layer_history[1] = "Waiting for message on API 1...\n"
        # self.layer_history[2] = "Waiting for message on API 2...\n"
        # self.layer_history[3] = "Waiting for message on API 3...\n"
        # self.layer_history[4] = "Waiting for message on API 4...\n"
        # self.layer_history[5] = "Waiting for message on API 5...\n"
        # self.layer_history[6] = "Waiting for message on API 6...\n"

        # Console API ScrollView and Label
        # self.scrollview_api0 = ScrollView()
        # self.label_api0 = Label(text=self.layer_history[0], size_hint_y=None)
        # self.label_api0.bind(texture_size=self.label_api0.setter('size'))
        # self.scrollview_api0.add_widget(self.label_api0)
        #
        # # API 1 ScrollView and Label
        # self.scrollview_api1 = ScrollView()
        # self.label_api1 = Label(text=self.layer_history[1], size_hint_y=None)
        # self.label_api1.bind(texture_size=self.label_api1.setter('size'))
        # self.scrollview_api1.add_widget(self.label_api1)
        #
        # # API 2 ScrollView and Label
        # self.scrollview_api2 = ScrollView()
        # self.label_api2 = Label(text=self.layer_history[2], size_hint_y=None)
        # self.label_api2.bind(texture_size=self.label_api2.setter('size'))
        # self.scrollview_api2.add_widget(self.label_api2)
        #
        # # API 3 ScrollView and Label
        # self.scrollview_api3 = ScrollView()
        # self.label_api3 = Label(text=self.layer_history[3], size_hint_y=None)
        # self.label_api3.bind(texture_size=self.label_api3.setter('size'))
        # self.scrollview_api3.add_widget(self.label_api3)
        #
        # # API 4 ScrollView and Label
        # self.scrollview_api4 = ScrollView()
        # self.label_api4 = Label(text=self.layer_history[4], size_hint_y=None)
        # self.label_api4.bind(texture_size=self.label_api4.setter('size'))
        # self.scrollview_api4.add_widget(self.label_api4)
        #
        # # API 5 ScrollView and Label
        # self.scrollview_api5 = ScrollView()
        # self.label_api5 = Label(text=self.layer_history[5], size_hint_y=None)
        # self.label_api5.bind(texture_size=self.label_api5.setter('size'))
        # self.scrollview_api5.add_widget(self.label_api5)
        #
        # # API 6 ScrollView and Label
        # self.scrollview_api6 = ScrollView()
        # self.label_api6 = Label(text=self.layer_history[6], size_hint_y=None)
        # self.label_api6.bind(texture_size=self.label_api6.setter('size'))
        # self.scrollview_api6.add_widget(self.label_api6)

        self.tab_console.add_widget(self.views[0])
        self.tab1.add_widget(self.views[1])
        self.tab2.add_widget(self.views[2])
        self.tab3.add_widget(self.views[3])
        self.tab4.add_widget(self.views[4])
        self.tab5.add_widget(self.views[5])
        self.tab6.add_widget(self.views[6])

        self.tab_panel.add_widget(self.tab_console)
        self.tab_panel.add_widget(self.tab1)
        self.tab_panel.add_widget(self.tab2)
        self.tab_panel.add_widget(self.tab3)
        self.tab_panel.add_widget(self.tab4)
        self.tab_panel.add_widget(self.tab5)
        self.tab_panel.add_widget(self.tab6)

        self.main_layout.add_widget(self.tab_panel)

        # Chatbox and Send button
        self.chatbox = TextInput(hint_text='Enter a message...')
        self.send_button = Button(text='Send', size_hint_x=None, width=100)
        self.send_button.bind(on_press=self.send_message)

        self.bottom_layout = BoxLayout(size_hint_y=None, height=44)
        self.bottom_layout.add_widget(self.chatbox)
        self.bottom_layout.add_widget(self.send_button)

        self.main_layout.add_widget(self.bottom_layout)

        return self.main_layout

    def update_label(self, layer_number, message):
        # Update the history for the given layer
        # label_attr = f"label_api{layer_number}"

        # Check if the label attribute exists
        if self.labels[layer_number]:
            self.history[layer_number] += message + '\n'
            self.labels[layer_number].text = self.history[layer_number]
        else:
            # Handle case where the layer doesn't have a matching label
            print(f"Error: Layer {layer_number} does not have a matching label attribute.")

        # if hasattr(self, self.labels[layer_number]):
        #     self.history[layer_number] += message + '\n'
        #     getattr(self, label_attr).text = self.history[layer_number]
        # else:
        #     # Handle case where the layer doesn't have a matching label
        #     print(f"Error: Layer {layer_number} does not have a matching label attribute.")

    def send_message(self, instance):
        message = self.chatbox.text
        if message:
            response = requests.post('http://127.0.0.1:1337/bot', json={'message': message})
            # Clear the chatbox after sending
            self.chatbox.text = ''


if __name__ == '__main__':
    Builder.load_file('kivy_theme.kv')
    # Run Flask API in a separate thread
    threading.Thread(target=run_flask_app).start()

    # Run Kivy App
    kivy_app = KivyApp()
    kivy_app.run()
