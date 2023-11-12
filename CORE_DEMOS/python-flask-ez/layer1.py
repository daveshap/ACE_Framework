from ace_layers import *


if __name__ == '__main__':
    openai.api_key = open_file('key_openai.txt').strip()
    response = ''
    while True:
        try:
            # FETCH FROM BUS
            north_bus = get_messages('north', 1)
            messages = format_messages(north_bus)
            
            # FORMAT FOR API
            conversation = list()
            conversation.append({'role': 'system', 'content': open_file('layer1.txt').replace('<<INTERNAL>>', response)})
            conversation.append({'role': 'user', 'content': messages})
            response, tokens = chatbot(conversation)
            chat_print(response)
            
            # POST TO BUS
            send_message('south', 1, response)
            
            # WAIT
            
        except Exception as oops:
            print(f'\n\nError in MAIN LOOP of LAYER 1: "{oops}"')
        sleep(5)