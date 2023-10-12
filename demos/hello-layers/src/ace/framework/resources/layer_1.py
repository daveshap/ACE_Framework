import time

from ace.framework.layer import Layer, LayerSettings
from ace.framework.prompts.identities import l1_identity
from jinja2 import Template

DECLARE_DONE_MESSAGE_COUNT = 5


class Layer1(Layer):

    def __init__(self):
        super().__init__()
        self.message_count = 0
        self.work_begun = False
        self.done = False

    @property
    def settings(self):
        return LayerSettings(
            name="layer_1",
            label="Aspirational",
            telemetry_subscriptions=[
                "user.encouragement",
            ],
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    def set_identity(self):
        self.identity = l1_identity

    def begin_work(self):
        self.log.info(f"{self.labeled_name} received command to begin work")
        self.work_begun = True

    def declare_done(self):
        message = self.build_message('system_integrity', message_type='done')
        self.push_exchange_message_to_publisher_local_queue(self.settings.system_integrity_data_queue, message)

    def process_layer_messages(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        time.sleep(5)
        self.message_count += 1
        self.log.info(f"{self.labeled_name} message count: {self.message_count}")
        # if self.message_count >= DECLARE_DONE_MESSAGE_COUNT:
        #     if not self.done:
        #         self.declare_done()
        #     return [], []

        # Create operation classifier prompt
        # Get operation classification
        # Parse operation classification for SOUTH
        # For each bus direction:
        # If classification is TAKE_ACTION, select appropriate southbound output message from outputs.py to render operations prompt
        # Render appropraite operations prompt from operation_descriptions.py
        # Create layer instruction prompt using l1_layer_instructions.py
        # Parse output messages into message types
        # Return messages
        messages_northbound = []
        messages_southbound = [
            {
                "type": "control",
                "message": "hello control"
            }
        ]
        return messages_northbound, messages_southbound

