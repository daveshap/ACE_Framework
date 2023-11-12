import time

from ace.framework.layer import Layer, LayerSettings
from ace.framework.llm.gpt import GptMessage
from ace.framework.util import parse_json
from ace.framework.enums.operation_classification_enum import OperationClassification
from jinja2 import Environment, FileSystemLoader
import os


class Layer3(Layer):

    @property
    def settings(self):
        return LayerSettings(
            name="layer_3",
            label="Agent Model",
            telemetry_subscriptions=[
                "environment.os.distribution.*",
                "environment.os.shell",
                "environment.os.resource_usage",
            ],
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    def process_layer_messages(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        identity_dir = self.get_identities_dir()
        identity_env = Environment(loader=FileSystemLoader(identity_dir))
        identity = identity_env.get_template("l3_identity.md").render()

        data_req_messages, control_req_messages = self.parse_req_resp_messages(request_messages)
        data_resp_messages, control_resp_messages = self.parse_req_resp_messages(response_messages)
        prompt_messages = {
            "data" : self.get_messages_for_prompt(data_messages),
            "data_resp" : self.get_messages_for_prompt(data_resp_messages),
            "control" : self.get_messages_for_prompt(control_messages),
            "control_resp" : self.get_messages_for_prompt(control_resp_messages),
            "data_req" : self.get_messages_for_prompt(data_req_messages),
            "control_req": self.get_messages_for_prompt(control_req_messages),
            "telemetry" : self.get_messages_for_prompt(telemetry_messages)
        }
        template_dir = self.get_template_dir()
        env = Environment(loader=FileSystemLoader(template_dir))
        operation_classifier = env.get_template("operation_classifier.md")
        ace_context = env.get_template("ace_context.md").render()
        op_classifier_prompt = operation_classifier.render(
            ace_context = ace_context,
            identity = identity,
            data = prompt_messages["data"],
            data_resp = prompt_messages["data_resp"],
            control = prompt_messages["control"],
            control_resp = prompt_messages["control_resp"]
        )

        llm_op_messages: [GptMessage] = [
            {"role": "user", "content": op_classifier_prompt},
        ]

        llm_op_response: GptMessage = self.llm._create_conversation_completion('gpt-3.5-turbo', llm_op_messages)
        llm_op_response_content = llm_op_response["content"].strip()
        op_classifier_log = env.get_template("op_log_message.md")
        op_log_message = op_classifier_log.render(
            op_classifier_req = op_classifier_prompt,
            op_classifier_resp = llm_op_response_content
        )
        self.resource_log(op_log_message)
        south_op_prompt, north_op_prompt = self.get_op_description(llm_op_response_content, "l3_south.md", "l3_north.md")

        layer_instructions = env.get_template("layer_instructions.md")

        layer3_instructions = layer_instructions.render(
            ace_context = ace_context,
            identity = identity,
            data = prompt_messages["data"],
            data_resp = prompt_messages["data_resp"],
            control = prompt_messages["control"],
            control_resp = prompt_messages["control_resp"],
            data_req = prompt_messages["data_req"],
            control_req = prompt_messages["control_req"],
            telemetry = prompt_messages["telemetry"],
            control_operation_prompt = south_op_prompt,
            data_operation_prompt =  north_op_prompt
        )

        llm_messages: [GptMessage] = [
            {"role": "user", "content": layer3_instructions},
        ]
        
        llm_response: GptMessage = self.llm._create_conversation_completion('gpt-3.5-turbo', llm_messages)
        llm_response_content = llm_response["content"].strip()
        layer_log_messsage = env.get_template("layer_log_message.md")
        log_message = layer_log_messsage.render(
            llm_req = layer3_instructions,
            llm_resp = llm_response_content
        )
        self.resource_log(log_message)
        llm_messages = parse_json(llm_response_content)
        messages_northbound, messages_southbound = self.parse_req_resp_messages(llm_messages)

        return messages_northbound, messages_southbound
