import layer
import top_layer as top
import openai
import os
from dotenv import load_dotenv
load_dotenv()

openai.api_key = os.getenv('OPENAI_API_KEY_1')

def stream_chat(stream):
	chat_message = ""
	for item in stream:
		chat_message += item

	return chat_message

if __name__ == "__main__":
	layers = [2, 3, 4, 5, 6]

	top_message = top.get_messages()
	top_response = stream_chat(top.chat_completion(top_message))
	top.save_response(top_response)
	print("top layer done")

	for layer_num in layers:
		message = layer.get_messages(layer_num)
		response = stream_chat(layer.chat_completion(layer_num, top_response))
		layer.save_response(layer_num, response)
		print(f"layer {layer_num} done")
