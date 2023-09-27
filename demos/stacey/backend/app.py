from flask import Flask, request, jsonify
from dotenv import load_dotenv
import gpt

load_dotenv()

app = Flask(__name__)


@app.route('/')
def root():
    return (
        'Hi! Stacey here. Yes, the backend is up and running! '
        'If you want to talk to me here you can do '
        '<a href="chat?message=hi">/chat?message=hi</a>'
    )


@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    model = data.get('model', 'gpt-3.5-turbo')
    conversation = data.get('conversation', [])

    try:
        response = gpt.create_chat_completion(model, conversation)
        return jsonify(response)
    except Exception as e:
        return jsonify({"error": str(e)}), 400


@app.route('/chat', methods=['GET'])
def chat_get():
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
        response = gpt.create_chat_completion('gpt-3.5-turbo', conversation)
        return response.content
    except Exception as e:
        return jsonify({"error": str(e)}), 400


if __name__ == '__main__':
    app.run(debug=True)
