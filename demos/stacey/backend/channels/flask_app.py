import traceback

from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

import config
from ace.ace_system import AceSystem
from tools.image_tool import replace_image_prompt_with_image_url_formatted_as_markdown


class FlaskApp:
    def __init__(self, ace_system, image_generator_function):
        self.app = Flask(__name__)
        CORS(self.app)
        self.ace_system = ace_system
        self.image_generator_function = image_generator_function

        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/')
        def root():
            return 'Hi! Stacey here. Yes, the backend is up and running! ' \
                   '<a href="chat?message=hi">/chat?message=hi</a>'

        @self.app.route('/chat', methods=['POST'])
        def chat():
            print("chat")
            data = request.json
            conversation = data.get('conversation', [])
            try:
                response = self.get_bot_response(conversation, "web")
                if response is None:
                    print("GPT decided to not respond to this")
                    return '', 204
                response_content = replace_image_prompt_with_image_url_formatted_as_markdown(
                    self.image_generator_function, response['content']
                )
                return jsonify({"role": response["role"], "content": response_content})
            except Exception as e:
                print(e)
                traceback_str = traceback.format_exc()  # Get the string representation of the traceback
                print("Traceback:", traceback_str)
                return jsonify({"error": str(e)}), 400

        @self.app.route('/chat', methods=['GET'])
        def chat_get():
            message = request.args.get('message')
            if not message:
                return jsonify({"error": "message parameter is required"}), 400
            conversation = [{"role": "user", "content": message}]
            try:
                response = self.get_bot_response(conversation, "web")
                return response.content
            except Exception as e:
                print(e)
                traceback_str = traceback.format_exc()  # Get the string representation of the traceback
                print("Traceback:", traceback_str)
                return jsonify({"error": str(e)}), 400

    def get_bot_response(self, conversation, communication_context):
        return self.ace_system.l3_agent.generate_response(conversation, communication_context)

    def run(self):
        self.app.run(port=5000, debug=False)


def main():
    from llm.gpt import GPT
    import os
    load_dotenv()
    openai_api_key = os.getenv('OPENAI_API_KEY')
    llm = GPT(openai_api_key)
    ace = AceSystem(llm, config.default_model)
    flask_app = FlaskApp(ace, llm.create_image)
    flask_app.run()


if __name__ == '__main__':
    main()

