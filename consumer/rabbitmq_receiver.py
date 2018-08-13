"""
    Consumes requests from provider(sender), sends result to provider(sender)
"""
from ast import literal_eval

import pika
import json
import time

from helper.builder import Builder  # pylint: disable=import-error
from helper.consumer_config import HOST, PORT, REQUEST_QUEUE, RESPONSE_QUEUE


class RabbitMQReceiver:
    """
    This class consumes requests from provider and sends result back to provider
    """
    def __init__(self):
        print('Connecting to rabbitmg...')
        retries = 30
        while True:
            try:
                # declare connection
                connection = pika.BlockingConnection(pika.ConnectionParameters(host=HOST, port=PORT))
                channel = connection.channel()
                break
            except pika.exceptions.ConnectionClosed as exc:
                if retries == 0:
                    print('Failed to connect!')
                    raise exc
                retries -= 1
                time.sleep(1)
        print('Successfully connected!')

        channel.queue_declare(queue=REQUEST_QUEUE)
        channel.queue_declare(queue=RESPONSE_QUEUE)

        print(' [*] Waiting for messages. To exit press CTRL+C')

        # declare consuming

        # CHANNEL.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback, no_ack=False, queue=REQUEST_QUEUE)

        # start waiting for request from provider(sender)
        channel.start_consuming()

    def worker(self, body):
        """

        :param body:
        :return: None, but sends result to provider(sender)
        """
        # decode request from provider(sender)
        body = literal_eval(body.decode())
        req_name = body['action']

        # gets response from API
        with Builder(body) as obj:
            # declare object with methods
            request = {
                'get_repo': obj.get_repo,
                'get_branches': obj.get_branches,
                'get_commits': obj.get_commits,
                'get_commits_by_branch': obj.get_commits_by_branch,
                'get_commit_by_hash': obj.get_commit_by_hash,
                'get_contributors': obj.get_contributors
            }
            if body['action'] == 'get_commit_by_hash':
                response = request[req_name](body['hash'])
            elif body['action'] == 'get_commits_by_branch':
                response = request[req_name](body['branch'])
            else:
                response = request[req_name]()

            print('response', response)

            # sends API response to provider(sender)
            # CHANNEL.basic_publish(exchange='',
            #                       routing_key=CALLBACK_QUEUE,
            #                       body=str(response))

            return response

    def callback(self, ch, method, props, body):
        """
            Consumes request from provider(sender)
        :param ch: unused param
        :param method: unused param
        :param props: unused param
        :param body: received message
        :return:
        """

        # print unused params to pass pylit check
        print(ch, method, props)

        print(" [x] Received %r" % (body,))

        # uses 'worker' function to get API response
        # and send it to provider(sender)
        response = self.worker(body)

        ch.basic_publish(exchange='',
                         routing_key=props.reply_to,
                         properties=pika.BasicProperties(correlation_id=props.correlation_id),
                         body=json.dumps(response))
        # to tell the server that message was properly handled
        ch.basic_ack(delivery_tag=method.delivery_tag)
