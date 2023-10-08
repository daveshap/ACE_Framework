from ace_layers import *


if __name__ == '__main__':
    openai.api_key = open_file('key_openai.txt').strip()
    response = ''
    while True:
        try:
            # FETCH FROM BUS
            north_bus = get_messages('north', 2)
            north_messages = format_messages(north_bus)
            south_bus = get_messages('south', 2)
            south_messages = format_messages(south_bus)
            messages = '''NORTH messages:\n%s\n\n\nSOUTH messages:\n%s''' % (north_messages, south_messages)
            
            
            # FORMAT FOR API
            conversation = list()
            conversation.append({'role': 'system', 'content': open_file('layer2.txt').replace('<<INTERNAL>>', response)})
            conversation.append({'role': 'user', 'content': messages})
            response, tokens = chatbot(conversation)
            chat_print(response)
            
            # POST TO BUS
            south_out = response.splitlines()[0].replace('SOUTH:').strip()
            north_out = response.splitlines()[1].replace('NORTH:').strip()
            send_message('south', 2, south_out)
            send_message('north', 2, north_out)
            
            # WAIT
            
        except Exception as oops:
            print(f'\n\nError in MAIN LOOP of LAYER 1: "{oops}"')
        sleep(5)