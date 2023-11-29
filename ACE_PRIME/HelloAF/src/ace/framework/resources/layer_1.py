from ace import constants
from ace.framework.layer import Layer, LayerSettings
from ace.framework.llm.gpt import GptMessage
from ace.framework.util import parse_json
from jinja2 import Environment, FileSystemLoader
import os


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

    def begin_work(self):
        self.log.info(f"{self.labeled_name} received command to begin work")
        self.work_begun = True

        identity_dir = self.get_identities_dir()
        identity_env = Environment(loader=FileSystemLoader(identity_dir))
        identity = identity_env.get_template("l1_identity.md").render()

        template_dir = self.get_template_dir()
        env = Environment(loader=FileSystemLoader(template_dir))
        l1_starting_instructions = env.get_template("l1_starting_instructions.md")
        ace_context = env.get_template("ace_context.md")
        layer1_instructions = l1_starting_instructions.render(
            ace_context=ace_context,
            identity=identity
        )

        llm_messages: [GptMessage] = [
            {"role": "user", "content": layer1_instructions},
        ]

        llm_response: GptMessage = self.llm._create_conversation_completion('gpt-3.5-turbo', llm_messages)
        llm_response_content = llm_response["content"].strip()
        layer_log_messsage = env.get_template("layer_log_message.md")
        log_message = layer_log_messsage.render(
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
        op_dir = self.get_operations_dir()
        outputs_dir = self.get_outputs_dir()
        op_env = Environment(loader=FileSystemLoader(op_dir))
        outputs_env = Environment(loader=FileSystemLoader(outputs_dir))
        match content:
            case "CREATE_REQUEST":
                op_description = op_env.get_template("create_request_data.md")
            case "TAKE_ACTION":
                take_action_data_l1 = op_env.get_template("take_action_data.md")
                southbound_outputs = outputs_env.get_template("l1_south.md")
                op_description = take_action_data_l1.render(layer_outputs=southbound_outputs)
            case _:
                op_description = op_env.get_template( "do_nothing_data.md")

        return op_description

    def process_layer_messages(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        identity_dir = self.get_identities_dir()
        identity_env = Environment(loader=FileSystemLoader(identity_dir))
        identity = identity_env.get_template("l1_identity.md").render()

        self.message_count += 1
        self.log.info(f"{self.labeled_name} message count: {self.message_count}")
        if self.message_count >= constants.LAYER_1_DECLARE_DONE_MESSAGE_COUNT:
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

        template_dir = self.get_template_dir()
        env = Environment(loader=FileSystemLoader(template_dir))
        l1_operation_classifier = env.get_template("l1_operation_classifier.md")
        ace_context = env.get_template("ace_context.md").render()
        op_classifier_prompt = l1_operation_classifier.render(
            ace_context=ace_context,
            identity=identity,
            data=prompt_messages["data"],
            data_resp=prompt_messages["data_resp"],
        )

        llm_op_messages: [GptMessage] = [
            {"role": "user", "content": op_classifier_prompt},
        ]

        llm_op_response: GptMessage = self.llm._create_conversation_completion('gpt-3.5-turbo', llm_op_messages)
        llm_op_response_content = llm_op_response["content"].strip()
        op_classifier_log = env.get_template("op_log_message.md")
        op_log_message = op_classifier_log.render(
            op_classifier_req=op_classifier_prompt,
            op_classifier_resp=llm_op_response_content
        )
        self.resource_log(op_log_message)
        op_prompt = self.get_op_description(llm_op_response_content)

        # If operation classifier says to do nothing, do not bother asking llm for a response
        op_dir = self.get_operations_dir()
        op_env = Environment(loader=FileSystemLoader(op_dir))
        do_nothing_data = op_env.get_template("do_nothing_data.md").render()
        if op_prompt == do_nothing_data:
            return [], []
        
        l1_layer_instructions = env.get_template("l1_layer_instructions.md")

        layer1_instructions = l1_layer_instructions.render(
            ace_context=ace_context,
            identity=identity,
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
        layer_log_messsage = env.get_template("layer_log_message.md")
        log_message = layer_log_messsage.render(
            llm_req=layer1_instructions,
            llm_resp=llm_response_content
        )
        self.resource_log(log_message)
        llm_messages = parse_json(llm_response_content)
        # There will never be northbound messages
        messages_northbound, messages_southbound = self.parse_req_resp_messages(llm_messages)
        self.resource_log(messages_southbound)

        return messages_northbound, messages_southbound
