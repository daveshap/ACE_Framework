# channels/flask/admin_routes.py
from flask import Blueprint, jsonify, current_app, request

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/bus_logs', methods=['GET'])
def get_bus_logs():
    ace_system = current_app.ace_system

    return jsonify({
        "northbound": ace_system.northbound_bus.message_log,
        "southbound": ace_system.southbound_bus.message_log
    })


@admin_bp.route('/publish_message', methods=['POST'])
def publish_message():
    try:
        # Extracting JSON data from the POST request
        data = request.get_json()

        if not data:
            return jsonify({"error": "Invalid JSON"}), 400

        # Extracting sender, message, and bus from the received JSON
        sender = data.get('sender')
        message = data.get('message')
        bus_name = data.get('bus')

        if not sender or not message or not bus_name:
            return jsonify({"error": "sender, message, and bus are required fields"}), 400

        ace_system = current_app.ace_system

        # Choosing the bus (northbound/southbound) to publish the message to, based on the received 'bus' field
        if bus_name == 'northbound':
            bus = ace_system.northbound_bus
        elif bus_name == 'southbound':
            bus = ace_system.southbound_bus
        else:
            return jsonify({"error": "Invalid bus name. Choose 'northbound' or 'southbound'."}), 400

        # Publishing the message to the selected bus
        bus.publish(sender, message)

        return jsonify({"success": True, "message": "Message published successfully"}), 200
    except Exception as e:
        print(e)
        return jsonify({"error": "An error occurred: " + str(e)}), 500
