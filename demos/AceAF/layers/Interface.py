from . import LAYER_REGISTRY


class Interface:

    def handle_outgoing(self):
        pass

    def handle_incoming(self):
        pass

    def collect_user_chat(self, message):
        # Process the user message
        # ...
        # Tag and store the message
        self.store_message(message, tag="new_input")
        # Trigger event for the relevant layer (e.g., L1)
        # LAYER_REGISTRY[1].event.set()

    def store_message(self, message, tag):
        # Store the message with the given tag
        pass
