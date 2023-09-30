from flask import Flask
from flask_cors import CORS

from channels.flask.admin_routes import admin_bp
from channels.flask.chat_routes import chat_bp


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


def main():
    from llm.gpt import GPT
    import os
    from dotenv import load_dotenv
    from ace.ace_system import AceSystem
    import config

    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')
    llm = GPT(openai_api_key)
    ace = AceSystem(llm, config.default_model)
    flask_app = FlaskApp(ace, llm.create_image)
    flask_app.run()


if __name__ == '__main__':
    main()