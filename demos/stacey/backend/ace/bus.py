# ace/bus.py
from pubsub import pub

class Bus:
    def __init__(self, name):
        self.name = name
        self.message_log = []

    def publish(self, sender, message):
        self.message_log.append((sender, message))
        pub.sendMessage(self.name, sender=sender, message=message)

    def subscribe(self, listener):
        pub.subscribe(listener, self.name)