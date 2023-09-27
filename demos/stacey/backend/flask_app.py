# flask_app.py
from dotenv import load_dotenv
from flask import Flask, request, jsonify
from flask_cors import CORS

import config
import gpt
from tools.image_tool import replace_image_prompt_with_image_url_formatted_as_markdown

load_dotenv()

app = Flask(__name__)
CORS(app)


@app.route('/')
def root():
    return (
        'Hi! Stacey here. Yes, the backend is up and running! '
        'If you want to talk to me here you can do '
        '<a href="chat?message=hi">/chat?message=hi</a>'
    )


@app.route('/chat', methods=['POST'])
def chat():
    """
    Sample input: {"model": "gpt-3.5-turbo", "conversation": [{"role": "user", "content": "Say hello to me"}]}
    Sample output: {"role": "assistant", "content": "Hello, how are you?"}
    """
    data = request.json
    model = data.get('model', 'gpt-3.5-turbo')
    conversation = data.get('conversation', [])

    # Insert Stacey's personality at the beginning of the conversation
    conversation.insert(0, {"role": "system", "content": config.system_message})

    try:
        response = gpt.create_chat_completion(model, conversation)
        response.content = replace_image_prompt_with_image_url_formatted_as_markdown(response.content)
        return jsonify(response)
    except Exception as e:
        print(e)
        return jsonify({"error": str(e)}), 400


@app.route('/chat', methods=['GET'])
def chat_get():
    """
    A simpler GET endpoint for quick testing.
    """
    message = request.args.get('message')
    if not message:
        return jsonify({"error": "message parameter is required"}), 400

    # For simplicity, creating a basic conversation with the user's message.
    # Modify as needed to suit your use case.
    conversation = [
        {"role": "system", "content": "You are a helpful assistant."},
        {"role": "user", "content": message}
    ]

    try:
        response = gpt.create_chat_completion(config.default_model, conversation)
        return response.content
    except Exception as e:
        return jsonify({"error": str(e)}), 400


def run():
    app.run(port=5000, debug=False)


if __name__ == '__main__':
    run()
