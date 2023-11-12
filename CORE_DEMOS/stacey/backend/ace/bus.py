class Bus:
    def __init__(self, name):
        self.name = name
        self.subscribers = []
        self.message_log = []

    def get_name(self):
        return self.name

    def messages(self):
        return list(self.message_log)

    def clear_messages(self):
        self.message_log.clear()

    async def publish(self, sender: str, message: str):
        print(f"Bus {self.name} was asked to publish message from {sender}: {message}")
        self.message_log.append({
            "sender": sender,
            "message": message
        })
        print(f"I have {len(self.subscribers)} subscribers")

        for subscriber in self.subscribers:
            print(f"Publishing to {subscriber}")
            await subscriber(sender, message)

    def subscribe(self, listener):
        self.subscribers.append(listener)
        print(f"Bus {self.name} was asked to subscribe listener {listener}")
