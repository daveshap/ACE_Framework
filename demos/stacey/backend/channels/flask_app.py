from flask import Flask
from flask_cors import CORS

from channels.admin_routes import admin_bp
from channels.chat_routes import chat_bp


class FlaskApp:
    def __init__(self, ace_system, image_generator_function):
        self.app = Flask(__name__)
        self.app.ace_system = ace_system
        self.app.image_generator_function = image_generator_function

        CORS(self.app)

        # Register the blueprints
        self.app.register_blueprint(chat_bp)
        self.app.register_blueprint(admin_bp)

        # Assign the ace_system and image_generator_function to the app context
        self.app.ace_system = ace_system
        self.app.image_generator_function = image_generator_function

        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def root():
            return 'Hi! Stacey here. Yes, the backend is up and running! ' \
                   '<a href="chat?message=hi">/chat?message=hi</a>'

    def run(self):
        self.app.run(port=5000, debug=False)
