import threading


class Bus:
    def __init__(self, name):
        self.name = name
        self.subscribers = []
        self.message_log = []
        self.lock = threading.Lock()

    def messages(self):
        with self.lock:
            return list(self.message_log)

    def clear_messages(self):
        with self.lock:
            self.message_log.clear()

    def publish(self, sender: str, message: str):
        print(f"{threading.current_thread().name} Bus {self.name} was asked to publish message from {sender}: {message}")
        with self.lock:
            self.message_log.append({
                "sender": sender,
                "message": message
            })
            print(f"I have {len(self.subscribers)} subscribers")

            for subscriber in self.subscribers:
                print(f"Publishing to {subscriber}")
                subscriber(sender, message)

    def subscribe(self, listener):
        with self.lock:
            self.subscribers.append(listener)
            print(f"{threading.current_thread().name} Bus {self.name} was asked to subscribe listener {listener}")
