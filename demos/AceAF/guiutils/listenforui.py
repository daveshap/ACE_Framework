# bot_api.py

from flask import Flask, request, jsonify


class BotApi:
    def __init__(self):
        self.app = Flask(__name__)
        self.setup_routes()

    def setup_routes(self):
        @self.app.route('/bot', methods=['POST'])
        def bot_endpoint():
            data = request.json
            message = data.get('message', '')
            # For this example, we'll just echo the received message.
            # In a real-world scenario, you can process the message or store it as needed.
            return jsonify({"received_message": message})

    def run(self, host='127.0.0.1', port=1337):
        self.app.run(host=host, port=port)


# Example usage:
if __name__ == "__main__":
    api = BotApi()
    api.run()
