from ace.framework.layer import Layer, LayerSettings
from ace.framework.llm.gpt import GptMessage
from ace.framework.util import parse_json
from jinja2 import Environment, FileSystemLoader


class Layer6(Layer):

    @property
    def settings(self):
        return LayerSettings(
            name="layer_6",
            label="Task Prosecution",
        )

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    def process_layer_messages(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        identity_dir = self.get_identities_dir()
        identity_env = Environment(loader=FileSystemLoader(identity_dir))
        identity = identity_env.get_template("l6_identity.md").render()

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
        ace_context = env.get_template("ace_context.md").render()

        layer_instructions = env.get_template("layer_instructions.md")

        layer6_instructions = layer_instructions.render(
            ace_context = ace_context,
            identity = identity,
            data = prompt_messages["data"],
            data_resp = prompt_messages["data_resp"],
            control = prompt_messages["control"],
            control_resp = prompt_messages["control_resp"],
            data_req = prompt_messages["data_req"],
            control_req = prompt_messages["control_req"],
            telemetry = prompt_messages["telemetry"],
        )

        llm_messages: [GptMessage] = [
            {"role": "user", "content": layer6_instructions},
        ]

        llm_response: GptMessage = self.llm.create_conversation_completion('gpt-3.5-turbo', llm_messages)
        llm_response_content = llm_response["content"].strip()
        layer_log_messsage = env.get_template("layer_log_message.md")
        log_message = layer_log_messsage.render(
            llm_req = layer6_instructions,
            llm_resp = llm_response_content
        )
        self.resource_log(log_message)
        llm_messages = parse_json(llm_response_content)
        # No sourthbound messages
        messages_northbound, _ = self.parse_req_resp_messages(llm_messages)

        return messages_northbound, []
