from base.base_layer import BaseLayer
import aio_pika
import logging
from settings import settings
from base.amqp.exchange import create_exchange
import time

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

class Layer6Prosecutor(BaseLayer):
    pass

    async def southbound_message_handler(self, message: aio_pika.IncomingMessage):

        logger.info(f"I'm the [{self.settings.role_name}] and I've received a [Southbound] message, here it is: {message.body.decode()}")

        exchange = await create_exchange(
            connection=self.connection,
            queue_name=self.settings.northbound_publish_queue,
        )
        # For now just forward the message southward
        time.sleep(1)
        message_body = aio_pika.Message(
            body=f"hello from {self.settings.role_name}...".encode(),
            delivery_mode=aio_pika.DeliveryMode.PERSISTENT
        )
        logger.info(f"I'm the [{self.settings.role_name}] and pretending have done something and sending a message [Northbound], here it is: {message.body.decode()}")
        await exchange.publish(
            message_body,
            routing_key=self.settings.northbound_publish_queue,
        )


        
        await message.ack()  # acknowledge the message


if __name__ == "__main__":
    layer = Layer6Prosecutor(settings)
    layer.run()
