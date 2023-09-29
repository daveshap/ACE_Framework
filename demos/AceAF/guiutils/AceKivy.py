# kivy_flask_app.py

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



@app.route('/L1Asiprational', methods=['POST'])
def api1():
    data = request.json
    message = data.get('message', '')
    kivy_app.update_label_api1(message)
    return jsonify({"status": "received"})


@app.route('/L2Strategy', methods=['POST'])
def api2():
    data = request.json
    message = data.get('message', '')
    kivy_app.update_label_api2(message)
    return jsonify({"status": "received"})


@app.route('/L3Agent', methods=['POST'])
def api3():
    data = request.json
    message = data.get('message', '')
    kivy_app.update_label_api3(message)
    return jsonify({"status": "received"})

@app.route('/L4Executive', methods=['POST'])
def api4():
    data = request.json
    message = data.get('message', '')
    kivy_app.update_label_api4(message)
    return jsonify({"status": "received"})

@app.route('/L5Cognitive', methods=['POST'])
def api5():
    data = request.json
    message = data.get('message', '')
    kivy_app.update_label_api5(message)
    return jsonify({"status": "received"})

@app.route('/L6Prosecution', methods=['POST'])
def api6():
    data = request.json
    message = data.get('message', '')
    kivy_app.update_label_api6(message)
    return jsonify({"status": "received"})

# Main Channel
@app.route('/console', methods=['POST'])
def console():
    data = request.json
    message = data.get('message', '')
    kivy_app.update_label_console(message)
    return jsonify({"status": "received"})

def run_flask_app():
    app.run(port=5000)


class KivyApp(App):

    def __init__(self, **kwargs):
        super(KivyApp, self).__init__(**kwargs)
        self.history_api1 = ""
        self.history_api2 = ""
        self.history_api3 = ""
        self.history_api4 = ""
        self.history_api5 = ""
        self.history_api6 = ""
        self.history_console = ""

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

        # Message histories
        self.history_console = "Waiting for message on console...\n"
        self.history_api1 = "Waiting for message on API 1...\n"
        self.history_api2 = "Waiting for message on API 2...\n"
        self.history_api3 = "Waiting for message on API 3...\n"
        self.history_api4 = "Waiting for message on API 4...\n"
        self.history_api5 = "Waiting for message on API 5...\n"
        self.history_api6 = "Waiting for message on API 6...\n"

        # API 1 ScrollView and Label
        self.scrollview_api1 = ScrollView()
        self.label_api1 = Label(text=self.history_api1, size_hint_y=None)
        self.label_api1.bind(texture_size=self.label_api1.setter('size'))
        self.scrollview_api1.add_widget(self.label_api1)

        # API 2 ScrollView and Label
        self.scrollview_api2 = ScrollView()
        self.label_api2 = Label(text=self.history_api2, size_hint_y=None)
        self.label_api2.bind(texture_size=self.label_api2.setter('size'))
        self.scrollview_api2.add_widget(self.label_api2)

        # API 3 ScrollView and Label
        self.scrollview_api3 = ScrollView()
        self.label_api3 = Label(text=self.history_api3, size_hint_y=None)
        self.label_api3.bind(texture_size=self.label_api3.setter('size'))
        self.scrollview_api3.add_widget(self.label_api3)

        # API 4 ScrollView and Label
        self.scrollview_api4 = ScrollView()
        self.label_api4 = Label(text=self.history_api4, size_hint_y=None)
        self.label_api4.bind(texture_size=self.label_api4.setter('size'))
        self.scrollview_api4.add_widget(self.label_api4)

        # API 5 ScrollView and Label
        self.scrollview_api5 = ScrollView()
        self.label_api5 = Label(text=self.history_api5, size_hint_y=None)
        self.label_api5.bind(texture_size=self.label_api5.setter('size'))
        self.scrollview_api5.add_widget(self.label_api5)

        # API 6 ScrollView and Label
        self.scrollview_api6 = ScrollView()
        self.label_api6 = Label(text=self.history_api6, size_hint_y=None)
        self.label_api6.bind(texture_size=self.label_api6.setter('size'))
        self.scrollview_api6.add_widget(self.label_api6)

        # Console API ScrollView and Label
        self.scrollview_console = ScrollView()
        self.label_console = Label(text=self.history_console, size_hint_y=None)
        self.label_console.bind(texture_size=self.label_console.setter('size'))
        self.scrollview_console.add_widget(self.label_console)

        self.tab1.add_widget(self.scrollview_console)
        self.tab1.add_widget(self.scrollview_api1)
        self.tab2.add_widget(self.scrollview_api2)
        self.tab3.add_widget(self.scrollview_api3)
        self.tab3.add_widget(self.scrollview_api4)
        self.tab3.add_widget(self.scrollview_api5)
        self.tab3.add_widget(self.scrollview_api6)

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

    def update_label_api1(self, message):
        self.history_api1 += message + '\n'
        self.label_api1.text = self.history_api1

    def update_label_api2(self, message):
        self.history_api2 += message + '\n'
        self.label_api2.text = self.history_api2

    def update_label_api3(self, message):
        self.history_api3 += message + '\n'
        self.label_api3.text = self.history_api3

    def update_label_api4(self, message):
        self.history_api4 += message + '\n'
        self.label_api4.text = self.history_api4

    def update_label_api5(self, message):
        self.history_api5 += message + '\n'
        self.label_api5.text = self.history_api5

    def update_label_api6(self, message):
        self.history_api6 += message + '\n'
        self.label_api6.text = self.history_api6

    def update_label_console(self, message):
        self.history_console += message + '\n'
        self.label_console.text = self.history_console

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
