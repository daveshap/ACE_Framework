from flask import Blueprint, jsonify, current_app

admin_bp = Blueprint('admin', __name__)


@admin_bp.route('/bus_logs', methods=['GET'])
def get_bus_logs():
    ace_system = current_app.ace_system

    return jsonify({
        "northbound": ace_system.northbound_bus.message_log,
        "southbound": ace_system.southbound_bus.message_log
    })
