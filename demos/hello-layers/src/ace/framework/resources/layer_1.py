import time

from ace.framework.layer import Layer, LayerSettings
from ace.framework.prompts.identities import l1_identity
from ace.framework.prompts.templates.l1_layer_instructions import l1_layer_instructions
from ace.framework.prompts.templates.l1_starting_instructions import l1_starting_instructions
from ace.framework.prompts.templates.l1_operation_classifier import l1_operation_classifier
from ace.framework.prompts.templates.log_messages import op_classifier_log, layer_messages_log
from ace.framework.prompts.ace_context import ace_context
from ace.framework.prompts.outputs import l1_southbound_outputs
from ace.framework.llm.gpt import GptMessage
from ace.framework.prompts.operation_descriptions import take_action_data_l1, do_nothing_data, create_request_data
from ace.framework.util import parse_json
from ace.framework.enums.operation_classification_enum import OperationClassification
from jinja2 import Template
import time

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
        layer1_instructions = l1_starting_instructions.render(
            ace_context=ace_context,
            identity=self.identity
        )

        llm_messages: [GptMessage] = [
            {"role": "user", "content": layer1_instructions},
        ]

        llm_response: GptMessage = self.llm._create_conversation_completion('gpt-3.5-turbo', llm_messages)
        llm_response_content = llm_response["content"].strip()
        log_message = layer_messages_log.render(
            llm_req=layer1_instructions,
            llm_resp=llm_response_content
        )
        self.resource_log(log_message)
        llm_messages = parse_json(llm_response_content)
        # There will never be northbound messages
        messages_northbound, messages_southbound = self.parse_req_resp_messages(llm_messages)

        if messages_northbound:
            for m in messages_northbound:
                message = self.build_message(self.northern_layer, message=m, message_type=m['type'])
                self.push_exchange_message_to_publisher_local_queue(f"northbound.{self.northern_layer}", message)
        if messages_southbound:
            for m in messages_southbound:
                message = self.build_message(self.southern_layer, message=m, message_type=m['type'])
                self.push_exchange_message_to_publisher_local_queue(f"southbound.{self.southern_layer}", message)

    def declare_done(self):
        self.log.info(f"{self.labeled_name} declaring work done")
        message = self.build_message('system_integrity', message_type='done')
        self.push_exchange_message_to_publisher_local_queue(self.settings.system_integrity_data_queue, message)

    def get_op_description(self, content):
        match content:
            case "CREATE_REQUEST":
                op_description = create_request_data
            case "TAKE_ACTION":
                op_description = take_action_data_l1.render(layer_outputs=l1_southbound_outputs)
            case _:
                op_description = do_nothing_data

        return op_description

    def process_layer_messages(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        self.message_count += 1
        self.log.info(f"{self.labeled_name} message count: {self.message_count}")
        if self.message_count >= DECLARE_DONE_MESSAGE_COUNT:
            if not self.done:
                self.declare_done()
                self.done = True
            return [], []
        data_req_messages, control_req_messages = self.parse_req_resp_messages(request_messages)
        data_resp_messages, control_resp_messages = self.parse_req_resp_messages(response_messages)
        prompt_messages = {
            "data": self.get_messages_for_prompt(data_messages),
            "data_resp": self.get_messages_for_prompt(data_resp_messages),
            "data_req": self.get_messages_for_prompt(data_req_messages),
            "telemetry": self.get_messages_for_prompt(telemetry_messages)
        }
        op_classifier_prompt = l1_operation_classifier.render(
            ace_context=ace_context,
            identity=self.identity,
            data=prompt_messages["data"],
            data_resp=prompt_messages["data_resp"],
        )

        llm_op_messages: [GptMessage] = [
            {"role": "user", "content": op_classifier_prompt},
        ]

        llm_op_response: GptMessage = self.llm._create_conversation_completion('gpt-3.5-turbo', llm_op_messages)
        llm_op_response_content = llm_op_response["content"].strip()
        op_log_message = op_classifier_log.render(
            op_classifier_req=op_classifier_prompt,
            op_classifier_resp=llm_op_response_content
        )
        self.resource_log(op_log_message)
        op_prompt = self.get_op_description(llm_op_response_content)

        # If operation classifier says to do nothing, do not bother asking llm for a response
        if op_prompt == do_nothing_data:
            return [], []

        layer1_instructions = l1_layer_instructions.render(
            ace_context=ace_context,
            identity=self.identity,
            data=prompt_messages["data"],
            data_resp=prompt_messages["data_resp"],
            data_req=prompt_messages["data_req"],
            telemetry=prompt_messages["telemetry"],
            operation_prompt=op_prompt
        )

        llm_messages: [GptMessage] = [
            {"role": "user", "content": layer1_instructions},
        ]

        llm_response: GptMessage = self.llm._create_conversation_completion('gpt-3.5-turbo', llm_messages)
        llm_response_content = llm_response["content"].strip()
        log_message = layer_messages_log.render(
            llm_req=layer1_instructions,
            llm_resp=llm_response_content
        )
        self.resource_log(log_message)
        llm_messages = parse_json(llm_response_content)
        # There will never be northbound messages
        messages_northbound, messages_southbound = self.parse_req_resp_messages(llm_messages)
        self.resource_log(messages_southbound)

        return messages_northbound, messages_southbound
