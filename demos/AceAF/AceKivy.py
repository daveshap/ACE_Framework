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

app = Flask(__name__)


@app.route('/api1', methods=['POST'])
def api1():
    data = request.json
    message = data.get('message', '')
    kivy_app.update_label_api1(message)
    return jsonify({"status": "received"})


@app.route('/api2', methods=['POST'])
def api2():
    data = request.json
    message = data.get('message', '')
    kivy_app.update_label_api2(message)
    return jsonify({"status": "received"})


@app.route('/api3', methods=['POST'])
def api3():
    data = request.json
    message = data.get('message', '')
    kivy_app.update_label_api3(message)
    return jsonify({"status": "received"})


def run_flask_app():
    app.run(port=5000)


class KivyApp(App):
    def build(self):
        self.main_layout = BoxLayout(orientation='vertical')
        self.tab_panel = TabbedPanel()

        self.tab_default = TabbedPanelItem(text='Default')
        self.tab1 = TabbedPanelItem(text='API 1')
        self.tab2 = TabbedPanelItem(text='API 2')
        self.tab3 = TabbedPanelItem(text='API 3')

        self.label_default = Label(text='This is the default tab.')
        self.label_api1 = Label(text='Waiting for message on API 1...')
        self.label_api2 = Label(text='Waiting for message on API 2...')
        self.label_api3 = Label(text='Waiting for message on API 3...')

        self.tab_default.add_widget(self.label_default)
        self.tab1.add_widget(self.label_api1)
        self.tab2.add_widget(self.label_api2)
        self.tab3.add_widget(self.label_api3)

        self.tab_panel.add_widget(self.tab_default)
        self.tab_panel.add_widget(self.tab1)
        self.tab_panel.add_widget(self.tab2)
        self.tab_panel.add_widget(self.tab3)

        self.main_layout.add_widget(self.tab_panel)

        # Chatbox and Send button
        self.chatbox = TextInput(hint_text='Enter a message...')
        self.send_button = Button(text='Send')
        self.send_button.bind(on_press=self.send_message)

        self.bottom_layout = BoxLayout(size_hint_y=None, height=44)
        self.bottom_layout.add_widget(self.chatbox)
        self.bottom_layout.add_widget(self.send_button)

        self.main_layout.add_widget(self.bottom_layout)

        return self.main_layout

    def update_label_api1(self, message):
        self.label_api1.text = message

    def update_label_api2(self, message):
        self.label_api2.text = message

    def update_label_api3(self, message):
        self.label_api3.text = message

    def send_message(self, instance):
        message = self.chatbox.text
        if message:
            response = requests.post('http://127.0.0.1:1337/bot', json={'message': message})
            # Clear the chatbox after sending
            self.chatbox.text = ''


if __name__ == '__main__':
    # Run Flask API in a separate thread
    threading.Thread(target=run_flask_app).start()

    # Run Kivy App
    kivy_app = KivyApp()
    kivy_app.run()
