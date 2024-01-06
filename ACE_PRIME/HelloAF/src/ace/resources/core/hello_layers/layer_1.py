import time
import asyncio

from ace import constants
from ace.framework.layer import Layer, LayerSettings
from ace.framework.llm.gpt import GptMessage
from ace.framework.util import parse_json
from ace.resources.core.hello_layers.util import get_template_dir, get_identities_dir
from jinja2 import Environment, FileSystemLoader


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

        identity_dir = get_identities_dir()
        identity_env = Environment(loader=FileSystemLoader(identity_dir))
        identity = identity_env.get_template("l1_identity.md").render()

        template_dir = get_template_dir()
        env = Environment(loader=FileSystemLoader(template_dir))
        l1_starting_instructions = env.get_template("l1_starting_instructions.md")
        ace_context = env.get_template("ace_context.md").render()
        layer1_instructions = l1_starting_instructions.render(
            ace_context=ace_context, identity=identity
        )

        llm_messages: [GptMessage] = [
            {"role": "user", "content": layer1_instructions},
        ]

        llm_response: GptMessage = self.llm.create_conversation_completion(
            "gpt-3.5-turbo", llm_messages
        )

        llm_response_content = llm_response.content.strip()
        layer_log_messsage = env.get_template("layer_log_message.md")
        log_message = layer_log_messsage.render(
            llm_req=layer1_instructions, llm_resp=llm_response_content
        )
        self.resource_log(log_message)
        llm_messages = parse_json(llm_response_content)
        # There will never be northbound messages
        _, messages_southbound = self.parse_req_resp_messages(llm_messages)

        if messages_southbound:
            for m in messages_southbound:
                message = self.build_message(
                    self.southern_layer, message=m, message_type=m["type"]
                )
                self.push_pathway_message_to_publisher_local_queue(
                    "southbound", message
                )
        time.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
        self.send_event_to_pathway("southbound", "execute")

    def declare_done(self):
        self.log.info(f"{self.labeled_name} declaring work done")
        message = self.build_message("system_integrity", message_type="done")
        self.push_exchange_message_to_publisher_local_queue(
            self.settings.system_integrity_data_queue, message
        )

    def process_layer_messages(
        self,
        control_messages,
        data_messages,
        request_messages,
        response_messages,
        telemetry_messages,
    ):
        identity_dir = get_identities_dir()
        identity_env = Environment(loader=FileSystemLoader(identity_dir))
        identity = identity_env.get_template("l1_identity.md").render()

        self.message_count += 1
        self.log.info(f"{self.labeled_name} message count: {self.message_count}")
        if self.message_count >= constants.LAYER_1_DECLARE_DONE_MESSAGE_COUNT:
            if not self.done:
                self.declare_done()
                self.done = True
            return [], []
        data_req_messages, control_req_messages = self.parse_req_resp_messages(
            request_messages
        )

        data_resp_messages, control_resp_messages = self.parse_req_resp_messages(
            response_messages
        )

        prompt_messages = {
            "data": self.get_messages_for_prompt(data_messages),
            "data_resp": self.get_messages_for_prompt(data_resp_messages),
            "data_req": self.get_messages_for_prompt(data_req_messages),
            "telemetry": self.get_messages_for_prompt(telemetry_messages),
        }

        template_dir = get_template_dir()
        env = Environment(loader=FileSystemLoader(template_dir))
        ace_context = env.get_template("ace_context.md").render()

        l1_layer_instructions = env.get_template("l1_layer_instructions.md")

        layer1_instructions = l1_layer_instructions.render(
            ace_context=ace_context,
            identity=identity,
            data=prompt_messages["data"],
            data_resp=prompt_messages["data_resp"],
            data_req=prompt_messages["data_req"],
            telemetry=prompt_messages["telemetry"],
        )

        llm_messages: [GptMessage] = [
            {"role": "user", "content": layer1_instructions},
        ]

        llm_response: GptMessage = self.llm.create_conversation_completion(
            self.settings.model, llm_messages
        )
        llm_response_content = llm_response["content"].strip()
        layer_log_messsage = env.get_template("layer_log_message.md")
        log_message = layer_log_messsage.render(
            llm_req=layer1_instructions, llm_resp=llm_response_content
        )
        self.resource_log(log_message)
        llm_messages = parse_json(llm_response_content)
        # There will never be northbound messages
        _, messages_southbound = self.parse_req_resp_messages(llm_messages)
        self.resource_log(messages_southbound)

        return [], messages_southbound

    async def handle_event(self, event, data):
        await super().handle_event(event, data)
        if event == "execute":
            self.agent_run_layer()
            await asyncio.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
            self.send_event_to_pathway("southbound", "execute")
