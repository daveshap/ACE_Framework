import time
import yaml
import aio_pika
from abc import abstractmethod
import asyncio
from threading import Thread
import os
from jinja2 import Environment, FileSystemLoader

from ace import constants
from ace.settings import Settings
from ace.framework.resource import Resource
from ace.framework.llm.gpt import GPT
from ace.framework.util import parse_json


class LayerSettings(Settings):
    mode: str = 'OpenAI'
    model: str = 'gpt-3.5-turbo'
    ai_retry_count: int = 3


class Layer(Resource):

    def __init__(self):
        super().__init__()
        self.layer_running = False

    async def post_connect(self):
        self.set_adjacent_layers()
        await self.subscribe_telemetry()
        self.set_llm()
        await self.register_busses()

    def post_start(self):
        self.subscribe_to_all_telemetry_namespaces()
        asyncio.run_coroutine_threadsafe(self.subscribe_debug_queue(), self.bus_loop)

    def pre_stop(self):
        self.layer_running = False
        asyncio.run_coroutine_threadsafe(self.unsubscribe_debug_queue(), self.bus_loop)

    async def pre_disconnect(self):
        await self.unsubscribe_telemetry()
        self.unsubscribe_from_all_telemetry_namespaces()
        await self.deregister_busses()

    def set_adjacent_layers(self):
        self.northern_layer = None
        self.southern_layer = None
        try:
            layer_index = self.settings.layers.index(self.settings.name)
            if layer_index > 0:
                self.northern_layer = self.settings.layers[layer_index - 1]
            if layer_index < len(self.settings.layers) - 1:
                self.southern_layer = self.settings.layers[layer_index + 1]
        except ValueError:
            message = f"Invalid layer name: {self.settings.name}"
            self.log.error(message, exc_info=True)
            raise ValueError(message)

    def set_llm(self):
        self.llm = GPT()

    async def register_busses(self):
        self.log.debug("Registering busses...")
        await self.subscribe_adjacent_layers()
        self.log.debug("Registered busses...")

    async def deregister_busses(self):
        self.log.debug("Deregistering busses...")
        await self.unsubscribe_adjacent_layers()
        self.log.debug("Deregistered busses...")

    @abstractmethod
    def process_layer_messages(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        pass

    def run_layer(self):
        self.layer_running = True
        Thread(target=self.run_layer_in_thread).start()

    def run_layers_debug_messages(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        if control_messages:
            self.log.debug(f"[{self.labeled_name}] RUN LAYER CONTROL MESSAGES: {control_messages}")
        if data_messages:
            self.log.debug(f"[{self.labeled_name}] RUN LAYER DATA MESSAGES: {data_messages}")
        if request_messages:
            self.log.debug(f"[{self.labeled_name}] RUN LAYER REQUEST MESSAGES: {request_messages}")
        if response_messages:
            self.log.debug(f"[{self.labeled_name}] RUN LAYER RESPONSE MESSAGES: {response_messages}")
        if telemetry_messages:
            self.log.debug(f"[{self.labeled_name}] RUN LAYER TELEMETRY MESSAGES: {telemetry_messages}")

    def parse_req_resp_messages(self, messages=None):
        messages = messages or []
        data_messages, control_messages = [], []
        for m in messages:
            if m['type'] == "DATA_RESPONSE" or m['type'] == "CONTROL_RESPONSE":
                m['type'] = 'response'
            elif m['type'] == "DATA_REQUEST" or m['type'] == "CONTROL_REQUEST":
                m['type'] = 'request'
            elif m['type'] == "DATA":
                m['type'] = 'data'
            elif m['type'] == "CONTROL":
                m['type'] = 'control'
            else:
                m['type'] = 'data'
        if messages:
            data_messages = [m for m in messages if m['direction']=="northbound"]
            control_messages = [m for m in messages if m['direction']=="southbound"]
        self.log.debug(f"[{self.labeled_name}] RETURNED CONTROL MESSAGES: {control_messages}")
        self.log.debug(f"[{self.labeled_name}] RETURNED DATA MESSAGES: {data_messages}")
        return data_messages, control_messages

    def get_messages_for_prompt(self, messages):
        self.log.debug(f"[{self.labeled_name}] MESSAGES: {messages}")
        if not messages:
            return "None"
        if messages[0]['type'] == 'telemetry':
            message_strings = [m['namespace'] + ': ' + m['data'] for m in messages]
        else:
            message_strings = [m['message'] for m in messages]
        result = " | ".join(message_strings)
        return result

    def get_template_dir(self):
        return os.path.join(os.path.dirname(__file__), "prompts/templates")

    def get_operations_dir(self):
        return os.path.join(os.path.dirname(__file__), "prompts/operations")

    def get_outputs_dir(self):
        return os.path.join(os.path.dirname(__file__), "prompts/outputs")

    def get_identities_dir(self):
        return os.path.join(os.path.dirname(__file__), "prompts/identities")

    def get_op_description(self, content, southbound_outputs_filename, nourthbound_outputs_filename):
        op_dir = self.get_operations_dir()
        outputs_dir = self.get_outputs_dir()
        op_env = Environment(loader=FileSystemLoader(op_dir))
        outputs_env = Environment(loader=FileSystemLoader(outputs_dir))
        operation_map = parse_json(content)
        south_op = operation_map["SOUTH"]
        north_op = operation_map["NORTH"]

        match south_op:
            case "CREATE_REQUEST":
                south_op_description = op_env.get_template("create_request_control.md").render()
            case "TAKE_ACTION":
                take_action_control = op_env.get_template("take_action_control.md")
                southbound_outputs = outputs_env.get_template(southbound_outputs_filename).render()
                south_op_description = take_action_control.render(layer_outputs=southbound_outputs)
            case _:
                south_op_description = op_env.get_template("do_nothing_control.md").render()
        match north_op:
            case "CREATE_REQUEST":
                north_op_description = op_env.get_template("create_request_data.md").render()
            case "TAKE_ACTION":
                take_action_data = op_env.get_template("take_action_data.md")
                northbound_outputs = outputs_env.get_template(nourthbound_outputs_filename)
                north_op_description = take_action_data.render(layer_outputs=northbound_outputs)
            case _:
                north_op_description = op_env.get_template("do_nothing_data.md").render()

        return south_op_description, north_op_description

    def debug_run_layer(self):
        control_messages, data_messages, request_messages, response_messages, telemetry_messages = self.get_all_local_messages()
        messages = {
            'control': control_messages,
            'data': data_messages,
            'request': request_messages,
            'response': response_messages,
            'telemetry': telemetry_messages,
        }
        total_messages = sum(len(x) for x in messages.values() if x)
        if total_messages > 0:
            self.debug_update_messages_state(messages)

    def debug_update_messages_state(self, messages):
        self.log.info(f"[{self.labeled_name}] received debug request to update messages state...")
        message = self.build_message('debug', message={'layer': self.settings.name, 'messages': messages}, message_type='layer_state')
        self.push_exchange_message_to_publisher_local_queue(self.settings.debug_data_queue, message)

    def debug_update_debug_state(self, **data):
        state = data['state']
        self.log.info(f"[{self.labeled_name}] received debug request to update debug state to: {state}")
        self.set_debug_state(state)
        message = self.build_message('debug', message={'layer': self.settings.name, 'state': state}, message_type='debug_state')
        self.push_exchange_message_to_publisher_local_queue(self.settings.debug_data_queue, message)

    def debug_run_layer_with_messages(self, **data):
        self.log.info(f"[{self.labeled_name}] received debug run layer request, messages: {data}")
        self.agent_run_and_publish(data['control'], data['data'], data['request'], data['response'], data['telemetry'])

    def get_all_local_messages(self):
        control_messages, data_messages = None, None
        if self.northern_layer:
            control_messages = self.get_messages_from_consumer_local_queue('control')
        if self.southern_layer:
            data_messages = self.get_messages_from_consumer_local_queue('data')
        request_messages = self.get_messages_from_consumer_local_queue('request')
        response_messages = self.get_messages_from_consumer_local_queue('response')
        telemetry_messages = self.get_messages_from_consumer_local_queue('telemetry')
        return control_messages, data_messages, request_messages, response_messages, telemetry_messages

    def agent_run_and_publish(self, control_messages, data_messages, request_messages, response_messages, telemetry_messages):
        self.log.info(f"[{self.labeled_name}] agent run and publish...")
        messages_northbound, messages_southbound = self.process_layer_messages(control_messages, data_messages, request_messages, response_messages, telemetry_messages)
        if messages_northbound and self.northern_layer:
            for m in messages_northbound:
                message = self.build_message(self.northern_layer, message=m, message_type=m['type'])
                self.push_exchange_message_to_publisher_local_queue(f"northbound.{self.northern_layer}", message)
        if messages_southbound and self.southern_layer:
            for m in messages_southbound:
                message = self.build_message(self.southern_layer, message=m, message_type=m['type'])
                self.push_exchange_message_to_publisher_local_queue(f"southbound.{self.southern_layer}", message)

    def agent_run_layer(self):
        control_messages, data_messages, request_messages, response_messages, telemetry_messages = self.get_all_local_messages()
        self.run_layers_debug_messages(control_messages,
                                       data_messages,
                                       request_messages,
                                       response_messages,
                                       telemetry_messages,
                                       )
        self.agent_run_and_publish(control_messages, data_messages, request_messages, response_messages, telemetry_messages)

    def run_layer_in_thread(self):
        while self.layer_running:
            if self.debug_mode:
                self.debug_run_layer()
                time.sleep(constants.DEBUG_LAYER_SLEEP_TIME)
            else:
                self.agent_run_layer()
                if not self.debug_mode:
                    time.sleep(constants.LAYER_SLEEP_TIME)

    async def send_message(self, direction, layer, message, delivery_mode=2):
        queue_name = self.build_layer_queue_name(direction, layer)
        if queue_name:
            self.log.debug(f"Send message: {self.labeled_name} ->  {queue_name}")
            exchange = self.build_exchange_name(queue_name)
            await self.publish_message(exchange, message)

    def is_ping(self, data):
        return data['type'] == 'ping'

    def is_pong(self, data):
        return data['type'] == 'pong'

    async def ping(self, direction, layer):
        self.log.info(f"Sending PING: {self.labeled_name} ->  {self.build_layer_queue_name(direction, layer)}")
        message = self.build_message(layer, message_type='ping')
        await self.send_message(direction, layer, message)

    async def handle_ping(self, direction, layer):
        response_direction = None
        layer = None
        if direction == 'northbound':
            response_direction = 'southbound'
            layer = self.southern_layer
        elif direction == 'southbound':
            response_direction = 'northbound'
            layer = self.northern_layer
        if response_direction and layer:
            message = self.build_message(layer, message_type='pong')
            await self.send_message(response_direction, layer, message)

    def schedule_post(self):
        asyncio.run_coroutine_threadsafe(self.post(), self.bus_loop)

    async def post(self):
        self.log.info(f"{self.labeled_name} received POST request")
        if self.northern_layer:
            await self.ping('northbound', self.northern_layer)
        if self.southern_layer:
            await self.ping('southbound', self.southern_layer)

    async def route_message(self, direction, message):
        try:
            data = yaml.safe_load(message.body.decode())
        except yaml.YAMLError as e:
            self.log.error(f"[{self.labeled_name}] could not parse [{direction}] message: {e}", exc_info=True)
            return
        data['direction'] = direction
        source_layer = data['resource']['source']
        if self.is_pong(data):
            self.log.info(f"[{self.labeled_name}] received a [pong] message from layer: {source_layer}")
            return
        elif self.is_ping(data):
            self.log.info(f"[{self.labeled_name}] received a [ping] message from layer: {source_layer}, bus direction: {direction}")
            return await self.handle_ping(direction, source_layer)
        self.push_message_to_consumer_local_queue(data['type'], data)

    async def telemetry_message_handler(self, message: aio_pika.IncomingMessage):
        self.log.debug(f"[{self.labeled_name}] received a [Telemetry] message")
        async with message.process():
            await self.route_message('telemetry', message)

    async def northbound_message_handler(self, message: aio_pika.IncomingMessage):
        self.log.debug(f"[{self.labeled_name}] received a [Northbound] message")
        async with message.process():
            await self.route_message('northbound', message)

    async def southbound_message_handler(self, message: aio_pika.IncomingMessage):
        self.log.debug(f"[{self.labeled_name}] received a [Southbound] message")
        async with message.process():
            await self.route_message('southbound', message)

    def subscribe_to_all_telemetry_namespaces(self):
        for namespace in self.settings.telemetry_subscriptions:
            self.telemetry_subscribe_to_namespace(namespace)

    def unsubscribe_from_all_telemetry_namespaces(self):
        for namespace in self.settings.telemetry_subscriptions:
            self.telemetry_unsubscribe_from_namespace(namespace)

    async def subscribe_telemetry(self):
        queue_name = self.build_telemetry_queue_name(self.settings.name)
        self.log.debug(f"{self.labeled_name} subscribing to {queue_name}...")
        self.consumers[queue_name] = await self.try_queue_subscribe(queue_name, self.telemetry_message_handler)

    async def unsubscribe_telemetry(self):
        queue_name = self.build_telemetry_queue_name(self.settings.name)
        if queue_name in self.consumers:
            queue, consumer_tag = self.consumers[queue_name]
            self.log.debug(f"{self.labeled_name} unsubscribing from {queue_name}...")
            await queue.cancel(consumer_tag)
            self.log.info(f"{self.labeled_name} unsubscribed from {queue_name}")

    async def subscribe_adjacent_layers(self):
        if self.northern_layer:
            southbound_queue = self.build_layer_queue_name('southbound', self.settings.name)
            self.log.debug(f"{self.labeled_name} subscribing to {southbound_queue}...")
            self.consumers[southbound_queue] = await self.try_queue_subscribe(southbound_queue, self.southbound_message_handler)
        if self.southern_layer:
            northbound_queue = self.build_layer_queue_name('northbound', self.settings.name)
            self.log.debug(f"{self.labeled_name} subscribing to {northbound_queue}...")
            self.consumers[northbound_queue] = await self.try_queue_subscribe(northbound_queue, self.northbound_message_handler)

    async def unsubscribe_adjacent_layers(self):
        northbound_queue = self.build_layer_queue_name('northbound', self.settings.name)
        southbound_queue = self.build_layer_queue_name('southbound', self.settings.name)
        if self.northern_layer and northbound_queue in self.consumers:
            queue, consumer_tag = self.consumers[northbound_queue]
            self.log.debug(f"{self.labeled_name} unsubscribing from {northbound_queue}...")
            await queue.cancel(consumer_tag)
            self.log.info(f"{self.labeled_name} unsubscribed from {northbound_queue}")
        if self.southern_layer and southbound_queue in self.consumers:
            queue, consumer_tag = self.consumers[southbound_queue]
            self.log.debug(f"{self.labeled_name} unsubscribing from {southbound_queue}...")
            await queue.cancel(consumer_tag)
            self.log.info(f"{self.labeled_name} unsubscribed from {southbound_queue}")
