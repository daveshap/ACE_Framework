from flask import Flask, request, Response
import top_layer
import layer
import os
import openai
from flask_cors import CORS, cross_origin
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY_1')

app = Flask(__name__)

CORS(app)

@app.route('/get_messages', methods=['GET'])
def get_messages():
    layer_num = int(request.args.get('layer'))
    if (layer_num > 1):
        return layer.get_messages(layer_num), 200
    else:
        return top_layer.get_messages(), 200


@app.route('/chat_completion', methods=['POST'])
def chat_completion():
    message = request.json
    layer_num = message['layer']
    messages = message['messages']
    stream = ''

    if (layer_num > 1):
        stream = layer.chat_completion(layer_num, messages)
    else:
        stream = top_layer.chat_completion(messages)
    
    return Response(stream, mimetype="text/event-stream")


@app.route('/save_response', methods=['POST'])
def save_response():
    message = request.json
    layer_num = message['layer']
    response = message['response']
    if (layer_num > 1):
        return layer.save_response(layer_num, response), 200
    else:
        return top_layer.save_response(response), 200


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)