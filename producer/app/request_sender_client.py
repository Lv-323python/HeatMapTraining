import pika
import uuid
import time
from producer.app.request_sender_client_config import HOST, PORT, RPC_QUEUE, CALLBACK_QUEUE


class RequestSenderClient:
    def __init__(self, host=HOST, port=PORT):
        self.host = host
        self.port = port
        self.response = None
        self.corr_id = None

        print('Connecting to rabbitmg...')
        RETRIES = 30
        while True:
            try:
                # declare connection
                self.connection = pika.BlockingConnection(pika.ConnectionParameters(host=self.host, port=self.port))
                self.channel = self.connection.channel()
                break
            except pika.exceptions.ConnectionClosed as exc:
                if RETRIES == 0:
                    print('Failed to connect!')
                    raise exc
                RETRIES -= 1
                time.sleep(1)
        print('Successfully connected!')

        # declare a queues
        queue = self.channel.queue_declare(queue=RPC_QUEUE)

        # declare a callback queue
        callback_queue = self.channel.queue_declare(queue=CALLBACK_QUEUE)  # only allow access by the current connection
        self.callback_queue = callback_queue.method.queue  # queue name
        self.channel.basic_consume(self.on_response, no_ack=True, queue=self.callback_queue)

    def on_response(self, ch, method, props, body):
        if self.corr_id == props.correlation_id:
            self.response = body

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
        print('Waiting for response...')
        while self.response is None:
            self.connection.process_data_events()
        print('Response received!')
        return self.response
