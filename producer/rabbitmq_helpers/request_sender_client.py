"""
This is a request sender client
"""
import time
import uuid
import pika
from rabbitmq_helpers.request_sender_client_config import HOST, PORT, RPC_QUEUE, CALLBACK_QUEUE
from general_helper.logger.log_config import LOG


# from general_helper.logger.log_error_decorators import try_except_decor


class RequestSenderClient:
    """
    This is a request sender client class
    """

    # @try_except_decor
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.response = None
        self.corr_id = None

        LOG.debug('Connecting to RabbitMQ...')

        retries = 30
        while True:
            try:
                # declare connection
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(
                    host=self.host,
                    port=self.port
                ))
                self.channel = self.connection.channel()
                break

            # except pika.exceptions.ConnectionClosed as exc:
            except BaseException as exc:
                if retries == 0:
                    LOG.debug('Failed to connect to RabbitMQ!')
                    raise exc

                retries -= 1
                time.sleep(1)

        LOG.debug('Successfully connected to RabbitMQ!')

        # declare a queues
        # pylint: disable=unused-variable
        queue = self.channel.queue_declare(queue=RPC_QUEUE)

        # declare a callback queue
        # only allow access by the current connection
        callback_queue = self.channel.queue_declare(queue=CALLBACK_QUEUE)
        self.callback_queue = callback_queue.method.queue  # queue name
        self.channel.basic_consume(self.on_response, no_ack=False, queue=self.callback_queue)

    def on_response(self, channel, method, props, body):
        """
        This is a method that takes positional parameters and
        :param channel:
        :param method:
        :param props:
        :param body:
        :return:
        """
        # pylint: disable=unused-argument
        if self.corr_id == props.correlation_id:
            self.response = body
            self.channel.stop_consuming()
            self.channel.basic_ack(delivery_tag=method.delivery_tag)

    # @try_except_decor
    def call(self, message):
        """
        This is a call method that takes message
        as a parameter and returns response
        :param message:
        :return: response
        """
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
        LOG.debug(f'Sent request: %s', message)
        LOG.debug('Waiting for response...')

        while self.response is None:
            self.channel.start_consuming()
        LOG.debug(f'Response received: %s', self.response)
        return self.response
