# response_generator.py
import pprint

from llm import gpt
import config

# This is a wrapper around GPT, to start providing some behavior around the responses.


def generate_response(model, conversation, communication_context):
    """
    Generates response considering the communication_context.
    :param model: Model name to use for OpenAI GPT.
    :param conversation: Conversation messages array.
    :param communication_context: String representing the communication context.
    :return: Generated response, for example {"role": "assistant", "content": "Hello, how are you?"}
    """

    # Replace {communication_channel} placeholder with actual communication_context in system message
    system_message = config.system_message.replace("{communication_channel}", communication_context)

    # Insert system message with replaced communication_context at the beginning of the conversation
    conversation.insert(0, {"role": "system", "content": system_message})

    # Generate response using gpt.create_chat_completion
    print(f"  Sending conversation to {model} in context {communication_context}:\n{pprint.pformat(conversation)}")

    response = gpt.create_chat_completion(model, conversation)

    print(f"  Got response: {response.content}")

    # Return None if content is empty, else return the response
    return None if not response['content'].strip() else response
