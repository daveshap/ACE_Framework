# channels/flask/flask_app.py
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from channels.web.admin_routes import admin_bp
from channels.web.chat_routes import chat_bp


class FlaskApp:
    def __init__(self, ace_system, image_generator_function):
        self.app = Flask(__name__)
        self.app.ace_system = ace_system
        self.app.image_generator_function = image_generator_function
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        CORS(self.app, resources={r"/*": {"origins": "*"}})
        # Register the blueprints
        self.app.register_blueprint(chat_bp)
        self.app.register_blueprint(admin_bp)

        # Assign the ace_system and image_generator_function to the app context
        self.app.ace_system = ace_system
        self.app.image_generator_function = image_generator_function

        self.setup_routes()

        self.setup_listeners()

    def setup_listeners(self):
        for bus in [self.app.ace_system.northbound_bus, self.app.ace_system.southbound_bus]:
            bus.subscribe(self.create_bus_listener(bus))

        for layer in self.app.ace_system.get_layers():
            layer.add_status_listener(self.create_layer_status_listener(layer))

    def create_bus_listener(self, bus):
        def listener(sender, message):
            try:
                print(f"flask_app detected message on bus from {sender}: {message}")
                self.socketio.emit(bus.get_name(), {'sender': sender, 'message': message})
            except Exception as e:
                print(f"Error in bus listener: {e}")
        return listener

    def create_layer_status_listener(self, layer):
        def listener(status):
            try:
                print(f"flask_app detected status change in layer {layer.get_id}: {status}")
                self.socketio.emit(f'layer-{layer.get_id()}-status', {'status': status.name})
            except Exception as e:
                print(f"Error in layer status listener: {e}")
        return listener

    def setup_routes(self):
        @self.app.route('/')
        def root():
            return 'Hi! Stacey here. Yes, the backend is up and running! ' \
                   '<a href="chat?message=hi">/chat?message=hi</a>'

    def run(self):
        self.socketio.run(
            self.app,
            port=5000,
            debug=False,
            allow_unsafe_werkzeug=True
        )

