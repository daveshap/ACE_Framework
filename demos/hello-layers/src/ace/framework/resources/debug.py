import aio_pika
import asyncio
import httpx
import yaml

from ace import constants
from ace.settings import Settings
from ace.framework.resource import Resource
from ace.debug_endpoint import DebugEndpoint


class DebugSettings(Settings):
    pass


class Debug(Resource):

    def __init__(self):
        super().__init__()
        self.debug_endpoint = DebugEndpoint(constants.DEFAULT_DEBUG_ENDPOINT_PORT, self.debug_endpoint_routes)

    @property
    def settings(self):
        return DebugSettings(
            name="debug",
            label="Debug",
        )

    @property
    def debug_endpoint_routes(self):
        return {
            'get': {
                '/layers-messages': self.get_layers_messages,
            },
            'post': {
                '/run-layer': self.run_layer,
            },
        }

    # TODO: Add valid status checks.
    def status(self):
        self.log.debug(f"Checking {self.labeled_name} status")
        return self.return_status(True)

    def setup_service(self):
        super().setup_service()
        self.debug_endpoint.start_endpoint()

    def shutdown_service(self):
        super().shutdown_service()
        self.debug_endpoint.stop_endpoint()

    async def post_connect(self):
        await self.subscribe_debug_data()

    def get_layers_messages(self):
        self.log.debug(f"{self.labeled_name} requesting updated messages for layers")
        asyncio.run_coroutine_threadsafe(self.update_layers_messages_state(), self.bus_loop)
        self.log.debug(f"{self.labeled_name} requested updated messages for layers")
        return {
            'success': True,
            'message': f"Requested updated messages for layers: {', '.join(self.settings.layers)}"
        }

    def run_layer(self, data):
        layer = data['layer']
        messages = data['messages']
        self.log.debug(f"{self.labeled_name} requesting run layer for layer: {layer}")
        asyncio.run_coroutine_threadsafe(self.run_layer_with_messages(layer, messages), self.bus_loop)
        self.log.debug(f"{self.labeled_name} requested run layer for layer: {layer}")
        return {
            'success': True,
            'message': f"Requested run layer for layer: {layer}",
            'data': data,
        }

    async def debug_pre_disconnect(self):
        await self.unsubscribe_debug_data()

    async def publish_message(self, queue_name, message, delivery_mode=2):
        message = aio_pika.Message(
            body=message,
            delivery_mode=delivery_mode
        )
        await self.publisher_channel.default_exchange.publish(message, routing_key=queue_name)

    async def execute_resource_command(self, resource, command, kwargs=None):
        kwargs = kwargs or {}
        self.log.debug(f"[{self.labeled_name}] sending command '{command}' to resource: {resource}")
        queue_name = self.build_debug_queue_name(resource)
        message = self.build_message(resource, message={'method': command, 'kwargs': kwargs}, message_type='command')
        await self.publish_message(queue_name, message)

    async def update_layers_messages_state(self):
        self.log.debug(f"{self.labeled_name} updating layers messages state")
        for layer in self.settings.layers:
            await self.update_layer_messages_state(layer)

    async def update_layer_messages_state(self, layer):
        self.log.info(f"[{self.labeled_name}] sending debug_update_messages_state command to layer: {layer}")
        await self.execute_resource_command(layer, 'debug_update_messages_state')

    async def run_layer_with_messages(self, layer, messages):
        self.log.info(f"[{self.labeled_name}] sending debug_run_layer_with_messages command to layer: {layer}")
        await self.execute_resource_command(layer, 'debug_run_layer_with_messages', messages)

    async def message_data_handler(self, message: aio_pika.IncomingMessage):
        async with message.process():
            body = message.body.decode()
        self.log.debug(f"[{self.labeled_name}] received a data message: {body}")
        try:
            data = yaml.safe_load(body)
        except yaml.YAMLError as e:
            self.log.error(f"[{self.labeled_name}] could not parse data message: {e}")
            return
        await self.process_debug_data(data)

    async def process_debug_data(self, data):
        self.log.debug(f"{self.labeled_name} processing debug data: {data}")
        if data['type'] == 'state':
            await self.post_layer_messages_update(data)

    async def post_layer_messages_update(self, data):
        layer = data['layer']
        messages = data['messages']
        self.log.debug(f"{self.labeled_name} POST layer update for layer: {layer}")
        data = {'layer': layer, 'messages': messages}
        await self.post_to_debug_ui('layer-messages', data)

    async def post_to_debug_ui(self, path, data):
        async with httpx.AsyncClient() as client:
            response = await client.post(f'http://localhost:{constants.DEFAULT_DEBUG_UI_ENDPOINT_PORT}/{path}', json=data)
            self.log.debug(f"{self.labeled_name} POST response from debug UI: {response.text}")

    async def subscribe_debug_data(self):
        self.log.debug(f"{self.labeled_name} subscribing to debug data queue...")
        queue_name = self.settings.debug_data_queue
        self.consumers[queue_name] = await self.try_queue_subscribe(queue_name, self.message_data_handler)
        self.log.info(f"{self.labeled_name} subscribed to debug data queue")

    async def unsubscribe_debug_data(self):
        queue_name = self.settings.debug_data_queue
        if queue_name in self.consumers:
            queue, consumer_tag = self.consumers[queue_name]
            self.log.debug(f"{self.labeled_name} unsubscribing from debug data queue...")
            await queue.cancel(consumer_tag)
            self.log.info(f"{self.labeled_name} unsubscribed from debug data queue")
