# ace/bus.py
from pubsub import pub


class Bus:
    def __init__(self, name):
        self.name = name
        self.message_log = []

    def publish(self, layer, message):
        self.message_log.append((layer, message))
        pub.sendMessage(self.name, message=message)

    def subscribe(self, listener):
        pub.subscribe(listener, self.name)