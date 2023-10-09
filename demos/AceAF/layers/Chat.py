from customagents.GenerateAgent import GenerateAgent
from customagents.ReflectAgent import ReflectAgent
from customagents.TheoryAgent import TheoryAgent
from customagents.ThoughtAgent import ThoughtAgent
from agentforge.utils.guiutils.listenforui import BotApi as ListenForUI
from agentforge.utils.guiutils.sendtoui import ApiClient
from agentforge.utils.storage_interface import StorageInterface
import re
from Interface import Interface


class Chatbot:

    storage = StorageInterface().storage_utils
    gethistory = Interface().get_chat_history
    send = Interface().save_chat_message
    log = Interface().output_message
    thou = ThoughtAgent()
    gen = GenerateAgent()
    theo = TheoryAgent()
    ref = ReflectAgent()
    chat_history = None
    result = None
    parsed_data = None
    memories = None
    chat_response = None
    message = None

    def __init__(self):
        self.chat_history = self.storage.select_collection("chat_history")

    def run(self, message):
        print(message)
        self.message = message

        # save message to chat history
        history = self.gethistory()

        # run thought agent
        self.thought_agent(message, history)

        # run generate agent
        self.gen_agent(message, history)

        # run theory agent
        self.theory_agent(message, history)

        # run reflect agent
        self.reflect_agent(message, history)

    def thought_agent(self, message, history):
        self.result = self.thou.run(user_message=message,
                                    history=history["documents"])
        self.log(3, f"Thought Agent:\n=====\n{self.result}\n=====\n")
        self.thought = self.parse_lines()
        print(f"self.thought: {self.thought}")
        cat = self.format_string(self.thought["Category"])
        self.memory_recall(cat, message)

    def gen_agent(self, message, history):
        self.result = self.gen.run(user_message=message,
                                   history=history["documents"],
                                   memories=self.memories,
                                   emotion=self.thought["Emotion"],
                                   reason=self.thought["Reason"],
                                   thought=self.thought["Inner Thought"])
        self.log(3, f"Generate Agent:\n=====\n{self.result}\n=====\n")
        self.generate = self.parse_lines()
        print(f"self.thought: {self.generate}")
        self.chat_response = self.result

    def theory_agent(self, message, history):
        self.result = self.theo.run(user_message=message,
                                    history=history["documents"])
        self.log(3, f"Theory Agent:\n=====\n{self.result}\n=====\n")
        self.theory = self.parse_lines()
        print(f"self.thought: {self.theory}")

    def reflect_agent(self, message, history):

        self.result = self.ref.run(user_message=message,
                                   history=history["documents"],
                                   memories=self.memories,
                                   emotion=self.thought["Emotion"],
                                   reason=self.thought["Reason"],
                                   thought=self.thought["Inner Thought"],
                                   what=self.theory["What"],
                                   why=self.theory["Why"],
                                   response=self.chat_response)
        self.log(3, f"Reflect Agent:\n=====\n{self.result}\n=====\n")
        self.reflection = self.parse_lines()
        print(f"self.thought: {self.reflection}")

        if self.reflection["Choice"] == "Respond":
            return self.chat_response
        elif self.reflection["Choice"] == "Nothing":
            return "No Response Provided"
        else:
            new_response = self.gen.run(user_message=message, history=history["documents"], memories=self.memories,
                                        emotion=self.thought["Emotion"], reason=self.thought["Reason"],
                                        thought=self.thought["Inner Thought"], what=self.theory["What"],
                                        why=self.theory["Why"], feedback=self.reflection["Reason"],
                                        response=self.chat_response)
            return new_response

    def save_memory(self, bot_response):
        size = self.storage.count_collection("chat_history")
        bot_message = f"Chatbot: {bot_response}"
        params = {
            "collection_name": "chat_history",
            "data": [bot_message],
            "ids": [str(size + 1)],
            "metadata": [{"id": size + 1}]
        }
        self.storage.save_memory(params)

    def chatman(self, message):
        size = self.storage.count_collection("chat_history")
        qsize = max(size - 10, 1)
        print(f"qsize: {qsize}")
        params = {
            "collection_name": "chat_history",
            "filter": {"id": {"$gte": qsize}}
        }
        history = self.storage.load_collection(params)
        user_message = f"User: {message}"
        print(f"history: {history}")
        params = {
            "collection_name": "chat_history",
            "data": [user_message],
            "ids": [str(size + 1)],
            "metadata": [{"id": size + 1}]
        }
        if size == 0:
            history["documents"].append("No Results!")
        self.storage.save_memory(params)
        ApiClient().send_message("layer_update", 0, f"User: {message}\n")
        return history

    def parse_lines(self):
        result_dict = {}
        lines = self.result.strip().split('\n')
        for line in lines:
            parts = line.split(':')
            if len(parts) == 2:
                key = parts[0].strip()
                value = parts[1].strip()
                result_dict[key] = value
        return result_dict

    def memory_recall(self, category, message):
        params = {
            "collection_name": category,
            "query": message
        }
        self.memories = self.storage.query_memory(params, 10)
        return self.memories

    def format_string(self, input_str):
        # Check if the input string length is between 3 and 63 characters
        if 3 <= len(input_str) <= 63:
            # Check if the string starts and ends with an alphanumeric character
            if input_str[0].isalnum() and input_str[-1].isalnum():
                # Check if the string contains only alphanumeric characters, underscores, or hyphens
                if re.match("^[a-zA-Z0-9_-]*$", input_str):
                    # Check if the string contains no two consecutive periods
                    if ".." not in input_str:
                        # Check if the string is not a valid IPv4 address
                        if not re.match(r'^\d+\.\d+\.\d+\.\d+$', input_str):
                            return input_str  # String meets all criteria

        return None  # String does not meet the criteria



if __name__ == '__main__':
    print("Starting")

    api = ListenForUI(callback=Chatbot().run)

    # Add a simple input loop to keep the main thread running
    while True:
        try:
            # Use input or sleep for some time, so the main thread doesn't exit immediately
            user_input = input("Press Enter to exit...")
            if user_input:
                break
        except KeyboardInterrupt:
            break
