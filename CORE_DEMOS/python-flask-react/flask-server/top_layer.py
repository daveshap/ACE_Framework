import ace_layers as ace


def get_messages():
    try:
        # FETCH FROM BUS
        north_bus = ace.get_messages('north', 1)
        return ace.format_messages(north_bus)
    except Exception as oops:
        print(f'\n\nError in GET_MESSAGES of LAYER 1: "{oops}"')


def chat_completion(messages):
    try:
        # FORMAT FOR API
        response = ace.get_response(1).strip()
        conversation = list()
        conversation.append({'role': 'system', 'content': ace.open_file('layer1.txt').replace('<<INTERNAL>>', response)})
        conversation.append({'role': 'user', 'content': messages})
        response = ace.chatbot(conversation)

        for item in response:
            if 'content' in item['choices'][0]['delta']:
                yield item['choices'][0]['delta']['content']
        
    except Exception as oops:
        print(f'\n\nError in CHAT_COMPLETION of LAYER 1: "{oops}"')


def save_response(response):
    try:
        ace.set_response(1, response)
        ace.post_message('south', 1, response)

        return "responses saved"
        
    except Exception as oops:
        print(f'\n\nError in SAVE_RESPONSE of LAYER 1: "{oops}"')
