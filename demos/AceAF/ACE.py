from agentforge.utils.storage_interface import StorageInterface
from layers.L1Aspirational import L1Aspirational
from layers.L2Strategy import L2Strategy
from layers.L3Agent import L3Agent
from layers.L4Executive import L4Executive
from layers.L5Cognitive import L5Cognitive
from layers.L6Prosecution import L6Prosecution
from layers.Interface import Interface
import keyboard
import threading
import time
from flask import Flask, jsonify, request
import uuid


class ACE:

    def __init__(self):
        self.storage = StorageInterface().storage_utils
        self.interface = Interface()

        # Initialize Flask app
        self.flask_app = Flask(__name__)
        self.init_flask_routes()

        # Start Flask app in a separate thread
        self.flask_thread = threading.Thread(target=self.run_flask_app)
        self.flask_thread.daemon = True
        self.flask_thread.start()

        self.layer_threads = {}
        self.layer_outputs = {}

        # Initializing layers
        self.layers = {
            1: L1Aspirational(),
            2: L2Strategy(),
            3: L3Agent(),
            4: L4Executive(),
            5: L5Cognitive(),
            6: L6Prosecution()
        }

        self.layer_threads = {}  # To hold the threads

        for layer_number, layer_instance in self.layers.items():
            thread = threading.Thread(target=layer_instance.stand_by)
            thread.daemon = True
            thread.start()

        print("\nAll Layers Initialized, ACE Running...\n")

    def run(self):
        # Trigger L1
        time.sleep(3)
        self.layers[1].trigger_event('InputUpdate')

        # Main loop
        while True:
            # Check for 'ESC' key press
            if keyboard.is_pressed('esc'):
                print("Escape key detected! Exiting...")
                break
            time.sleep(15)

    def init_layer(self, layer_number):
        try:
            self.layers[layer_number].stand_by()
        except Exception as e:
            print(f"Error in layer {layer_number}: {e}")

    def init_flask_routes(self):
        @self.flask_app.route('/bot', methods=['POST'])
        def home():
            message = request.json.get('message')
            self.interface.save_chat_message(respondent="User", message=message)
            # trigger layer 3 to check chat history
            return jsonify({"received_message": message})

    def run_flask_app(self):
        self.flask_app.run(port=5001)


if __name__ == '__main__':
    ACE().run()
