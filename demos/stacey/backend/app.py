# app.py
from flask import Flask, request, jsonify
from dotenv import load_dotenv
import gpt

load_dotenv()

app = Flask(__name__)

@app.route('/chat', methods=['POST'])
def chat():
    data = request.json
    model = data.get('model', 'gpt-3.5-turbo')  # Use 'gpt-3.5-turbo' as default model
    conversation = data.get('conversation', [])

    try:
        response = gpt.create_chat_completion(model, conversation)
        return jsonify({"role": "assistant", "content": response})
    except Exception as e:
        return jsonify({"error": str(e)}), 400

if __name__ == '__main__':
    app.run(debug=True)
