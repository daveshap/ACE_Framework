import unittest

from ace.bus import Bus


class TestBus(unittest.TestCase):

    def test_one_bus_one_subscriber(self):
        bus = Bus('bus1')
        messages = []
        bus.subscribe(lambda sender, message: messages.append((sender, message)))
        bus.publish('sender1', 'message1')
        self.assertEqual(messages, [('sender1', 'message1')])

    def test_two_buses_one_subscriber(self):
        bus1 = Bus('bus1')
        bus2 = Bus('bus2')
        messages = []
        bus1.subscribe(lambda sender, message: messages.append((sender, message)))
        bus1.publish('sender1', 'message1')
        bus2.publish('sender2', 'message2')
        self.assertEqual(messages, [('sender1', 'message1')])

    def test_one_bus_two_subscribers(self):
        bus = Bus('bus1')
        messages1 = []
        messages2 = []
        bus.subscribe(lambda sender, message: messages1.append((sender, message)))
        bus.subscribe(lambda sender, message: messages2.append((sender, message)))
        bus.publish('sender1', 'message1')
        self.assertEqual(messages1, [('sender1', 'message1')])
        self.assertEqual(messages2, [('sender1', 'message1')])


if __name__ == '__main__':
    unittest.main()
