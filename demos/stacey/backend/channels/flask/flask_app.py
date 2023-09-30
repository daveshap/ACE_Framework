# channels/flask/flask_app.py
from flask import Flask
from flask_cors import CORS
from flask_socketio import SocketIO

from channels.flask.admin_routes import admin_bp
from channels.flask.chat_routes import chat_bp
from util import get_environment_variable


class FlaskApp:
    def __init__(self, ace_system, image_generator_function):
        self.app = Flask(__name__)
        self.app.ace_system = ace_system
        self.app.image_generator_function = image_generator_function
        self.socketio = SocketIO(self.app, cors_allowed_origins="*")

        CORS(self.app)

        # Register the blueprints
        self.app.register_blueprint(chat_bp)
        self.app.register_blueprint(admin_bp)

        # Assign the ace_system and image_generator_function to the app context
        self.app.ace_system = ace_system
        self.app.image_generator_function = image_generator_function

        self.setup_routes()

        self.setup_background_tasks(ace_system)

    def setup_background_tasks(self, ace_system):
        def background_task(bus):
            @bus.subscribe
            def listener(sender, message):
                print(f"flask_app detected message on bus from {sender}: {message}")
                self.socketio.emit(bus.name, {'sender': sender, 'message': message})

        background_task(ace_system.northbound_bus)
        background_task(ace_system.southbound_bus)

        # hardcoded to 1 layer for now.
        def status_listener(status):
            print(f"flask_app detected status change: {status}")
            self.socketio.emit('layer-1-status', {'status': status.name})

        ace_system.l1_aspirational_layer.add_status_listener(status_listener)

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


def main():
    from llm.gpt import GPT
    from dotenv import load_dotenv
    from ace.ace_system import AceSystem
    import config

    load_dotenv()
    openai_api_key = get_environment_variable('OPENAI_API_KEY')
    llm = GPT(openai_api_key)
    ace = AceSystem(llm, config.default_model)
    ace.start()
    flask_app = FlaskApp(ace, llm.create_image)
    flask_app.run()


if __name__ == '__main__':
    main()