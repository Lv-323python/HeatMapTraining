import pika
import uuid
import time
from rabbitmq_helpers.request_sender_client_config import HOST, PORT, RPC_QUEUE, CALLBACK_QUEUE
from general_helper.logger.log_config import LOG
from general_helper.logger.log_error_decorators import try_except_decor


class RequestSenderClient:
    @try_except_decor
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.response = None
        self.corr_id = None

        LOG.info('Connecting to RabbitMQ...')

        retries = 30
        while True:
            try:
                # declare connection
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
                self.channel = self.connection.channel()
                break

            # except pika.exceptions.ConnectionClosed as exc:
            except BaseException as exc:
                if retries == 0:
                    LOG.info('Failed to connect to RabbitMQ!')
                    raise exc

                retries -= 1
                time.sleep(1)

        LOG.info('Successfully connected to RabbitMQ!')

        # declare a queues
        queue = self.channel.queue_declare(queue=RPC_QUEUE)

        # declare a callback queue
        callback_queue = self.channel.queue_declare(queue=CALLBACK_QUEUE)  # only allow access by the current connection
        self.callback_queue = callback_queue.method.queue  # queue name
        self.channel.basic_consume(self.on_response, no_ack=False, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body
            self.channel.stop_consuming()
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

    @try_except_decor
    def call(self, message):
        self.corr_id = str(uuid.uuid4())

        self.channel.basic_publish(
            exchange='',
            routing_key=RPC_QUEUE,
            properties=pika.BasicProperties(
                reply_to=self.callback_queue,
                correlation_id=self.corr_id,
            ),
            body=message
        )
        LOG.info(f'Sent request: {message}')
        LOG.info('Waiting for response...')

        while self.response is None:
            self.channel.start_consuming()
        LOG.info(f'Response received: {self.response}')
        return self.response
