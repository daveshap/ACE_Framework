from flask import Flask, request
import yaml
import time
import os
import glob


app = Flask(__name__)



@app.route('/message', methods=['POST'])
def post_message():
    message = request.json
    message['timestamp'] = time.time()
    with open(f"/logs/log_{message['timestamp']}_{message['bus']}_{message['layer']}.yaml", 'w', encoding='utf-8') as file:
        yaml.dump(message, file)
    print(message['bus'], message['layer'], message['message'])
    return 'Message received', 200



@app.route('/message', methods=['GET'])
def get_messages():
    bus = request.args.get('bus')
    layer = int(request.args.get('layer'))
    files = glob.glob('/logs/*.yaml')
    messages = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            message = yaml.safe_load(f)
            messages.append(message)
    if bus == 'north':
        filtered_messages = [m for m in messages if m['bus'] == 'north' and m['layer'] > layer]
    else:
        filtered_messages = [m for m in messages if m['bus'] == 'south' and m['layer'] < layer]
    sorted_messages = sorted(filtered_messages, key=lambda m: m['timestamp'], reverse=True)
    return {'messages': sorted_messages[:20]}, 200



if __name__ == '__main__':
    app.run(host='0.0.0.0', port=900, debug=True)
