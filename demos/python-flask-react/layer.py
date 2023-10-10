import ace_layers as ace

def get_messages(layer_num):
    try:
        # FETCH FROM BUS
        north_bus = ace.get_messages('north', layer_num)
        north_messages = ace.format_messages(north_bus)
        south_bus = ace.get_messages('south', layer_num)
        south_messages = ace.format_messages(south_bus)

        return '''NORTH messages:\n%s\n\n\nSOUTH messages:\n%s''' % (north_messages, south_messages)
    except Exception as oops:
        print(f'\n\nError in GET_MESSAGES in LAYER {layer_num}: "{oops}"')


def chat_completion(layer_num, messages):
    try:
        # FORMAT FOR API
        response = ace.get_response(layer_num).strip()
        conversation = list()
        conversation.append({'role': 'system', 'content': ace.open_file(f"layer{layer_num}.txt").replace('<<INTERNAL>>', response)})
        conversation.append({'role': 'user', 'content': messages})
        response = ace.chatbot(conversation)

        for item in response:
            if 'content' in item['choices'][0]['delta']:
                yield item['choices'][0]['delta']['content']

    except Exception as oops:
        print(f'\n\nError in CHAT_COMPLETION in LAYER {layer_num}: "{oops}"')


def save_response(layer_num, response):
    try:
        # POST TO BUS
        ace.set_response(layer_num, response)
        south_out = response.splitlines()[0].replace('SOUTH:','').strip()
        north_out = response.splitlines()[1].replace('NORTH:','').strip()
        ace.post_message('south', layer_num, south_out)
        ace.post_message('north', layer_num, north_out)
        
    except Exception as oops:
        print(f'\n\nError in SAVE_RESPONSE of LAYER {layer_num}: "{oops}"')