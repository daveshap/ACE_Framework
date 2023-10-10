from ace.framework.layer import Layer, LayerSettings
from ace.framework.prompts.identities import l2_identity
from ace.framework.prompts.templates.layer_instructions import layer_instructions
from ace.framework.prompts.templates.operation_classifier import operation_classifier
from ace.framework.prompts.ace_context import ace_context
from ace.framework.prompts.outputs import l2_northbound_outputs, l2_southbound_outputs
import ace.framework.prompts.operation_descriptions


class Layer2(Layer):

    @property
    def settings(self):
        return LayerSettings(
            name="layer_2",
            label="Global Strategy",
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    def set_identity(self):
        self.identity=l2_identity
    
    def parse_req_resp_messages(self, messages):
        data_messages = list(filter(lambda m: m.direction == "northbound"), messages)
        control_messages = list(filter(lambda m: m.direction == "southbound"), messages)
        return data_messages, control_messages

    def get_message_strings(self, messages):
        return map(lambda x: x.text, messages)

    def process_layer_messages(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        # Create operation classifier prompt
        # Get operation classification
        # Parse operation classification for SOUTH
        # For each bus direction:
        #   If classification is TAKE_ACTION, select appropriate southbound output message from outputs.py to render operations prompt
        #   Render appropraite operations prompt from operation_descriptions.py
        # Create layer instruction prompt using layer_instructions.py
        # Parse output messages into message types 
        # Return messages
        time.sleep(5)
        messages_northbound = [
            {
                "type": "data",
                "message": "hello data"
            }
        ]
        messages_southbound = [
            {
                "type": "control",
                "message": "hello control"
            }
        ]
        return messages_northbound, messages_southbound