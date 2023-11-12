import openai
import yaml
from time import time, sleep
from datetime import datetime
import textwrap
import time
from functools import wraps
import glob
import os
from pathlib import Path

###      util functions

def retry(wait_time=360, max_retries=3):
    def decorator(func):
        @wraps(func)
        def wrapper(*args, **kwargs):
            for i in range(max_retries):
                try:
                    return func(*args, **kwargs)
                except Exception as e:
                    if i == max_retries - 1:  # If it's the last retry, raise the exception
                        raise
                    print(f"\n\nError: {e}. Retrying in {wait_time} seconds...")
                    time.sleep(wait_time)
        return wrapper
    return decorator


###     file operations


def save_file(filepath, content):
    output_file = Path(filepath)
    output_file.parent.mkdir(exist_ok=True, parents=True)
    output_file.write_text(content)


def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8', errors='ignore') as infile:
        return infile.read()


def get_message_logs(files):
    messages = []
    for file in files:
        with open(file, 'r', encoding='utf-8') as f:
            message = yaml.safe_load(f)
            messages.append(message)

    return messages


###     API functions

def get_response(layer_num):
    try:
        return open_file(f"logs/layer{layer_num}/response.txt")
    except Exception as oops:
        print(f'\n\nfile does not exist yet, proceed to return empty string')
        return ""


def set_response(layer_num, content):
    return save_file(f"logs/layer{layer_num}/response.txt", content)


def post_message(bus, layer, message):
    body = {
        'bus': bus,
        'layer': layer,
        'message': message,
        'timestamp': time.time()
    }
    filename = f"logs/layer{body['layer']}/log_{body['timestamp']}_{body['bus']}_{body['layer']}.yaml"
    os.makedirs(os.path.dirname(filename), exist_ok=True)
    with open(filename, 'w', encoding='utf-8') as file:
        yaml.dump(body, file)


def get_messages(bus, layer):
    if bus == 'north':
        files = glob.glob(f'logs/layer{layer + 1}/*.yaml')
        messages = get_message_logs(files)
        filtered_messages = [m for m in messages if m['bus'] == 'north' and m['layer'] > layer]
    else:
        files = glob.glob(f'logs/layer{layer - 1}/*.yaml') if layer > 1 else []
        messages = get_message_logs(files)
        filtered_messages = [m for m in messages if m['bus'] == 'south' and m['layer'] < layer]
    sorted_messages = sorted(filtered_messages, key=lambda m: m['timestamp'], reverse=True)

    return sorted_messages[:1]


def format_messages(messages):
    formatted_messages = []
    for message in messages:
        time = datetime.fromtimestamp(message['timestamp']).strftime('%Y-%m-%d %H:%M:%S')
        bus = message['bus']
        layer = message['layer']
        text = message['message']
        formatted_message = f'{time} - {bus} - Layer {layer} - {text}'
        formatted_messages.append(formatted_message)
    return '\n'.join(formatted_messages)
    
    
@retry()
def chatbot(conversation, model="gpt-4", temperature=0, max_tokens=2000):
    try:
        response = openai.ChatCompletion.create(model=model, messages=conversation, temperature=temperature, max_tokens=max_tokens, stream=True)
        
        return response
    except Exception as oops:
        print(f'\n\nError communicating with OpenAI: "{oops}"')
        raise oops


def chat_print(text):
    formatted_lines = [textwrap.fill(line, width=120, initial_indent='    ', subsequent_indent='    ') for line in text.split('\n')]
    formatted_text = '\n'.join(formatted_lines)
    print('\n\n\nLAYER:\n\n%s' % formatted_text)

