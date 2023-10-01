# channels/flask/chat_routes.py
import traceback

from flask import Blueprint, request, jsonify, current_app

from tools.image_tool import replace_image_prompt_with_image_url_formatted_as_markdown

chat_bp = Blueprint('chat', __name__)


@chat_bp.route('/chat', methods=['POST'])
def chat():
    # Assuming the FlaskApp instance is set to the app's context.
    ace_system = current_app.ace_system
    image_generator_function = current_app.image_generator_function

    data = request.json
    conversation = data.get('conversation', [])
    try:
        response = ace_system.l3_agent.generate_response(conversation, "web")
        if response is None:
            return '', 204
        response_content = replace_image_prompt_with_image_url_formatted_as_markdown(
            image_generator_function, response['content']
        )
        return jsonify({"role": response["role"], "content": response_content})
    except Exception as e:
        traceback_str = traceback.format_exc()
        return jsonify({"error": str(e), "traceback": traceback_str}), 400


@chat_bp.route('/chat', methods=['GET'])
def chat_get():
    ace_system = current_app.ace_system

    message = request.args.get('message')
    if not message:
        return jsonify({"error": "message parameter is required"}), 400
    conversation = [{"role": "user", "content": message}]
    try:
        response = ace_system.l3_agent.generate_response(conversation, "web")
        return response.content
    except Exception as e:
        traceback_str = traceback.format_exc()
        return jsonify({"error": str(e), "traceback": traceback_str}), 400
