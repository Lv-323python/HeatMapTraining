"""
    Consumes requests from provider(sender), sends result to provider(sender)
"""

import json
import time
import pika
import pika.exceptions

# temporary fix import error
# import sys
# sys.path.append('../')


from general_helper.logger.log_config import LOG
from general_helper.logger.log_error_decorators import try_except_decor
# from helper.redis_request_sender import RedisRequestSender
#from helper.mongodb_request_sender import MongoDBRequestSender
from helper.builder import Builder
from helper.consumer_config import HOST, PORT, REQUEST_QUEUE, RESPONSE_QUEUE
from helper.mongo_helpers import mongo_store


class RabbitMQReceiver:
    """
    This class consumes a request from the 'sender', receives an API response
and     and sends the result back to the provider
    """

    @try_except_decor
    def __init__(self):

        LOG.debug('Connecting to RabbitMQ...')
        retries = 30
        while True:
            try:
                # declare connection
                connection = pika.BlockingConnection(
                    pika.ConnectionParameters(host=HOST, port=PORT))

                #  channel
                channel = connection.channel()
                break

            except pika.exceptions.ConnectionClosed as exc:
                if retries == 0:
                    LOG.error('Failed to connect to RabbitMQ...')
                    raise exc
                retries -= 1
                time.sleep(1)
        LOG.debug('Successfully connected to RabbitMQ!')

        channel.queue_declare(queue=REQUEST_QUEUE)
        channel.queue_declare(queue=RESPONSE_QUEUE)

        LOG.debug(' [*] Waiting for request...')

        # declare consuming
        # CHANNEL.basic_qos(prefetch_count=1)
        channel.basic_consume(self.callback, no_ack=False, queue=REQUEST_QUEUE)

        # start waiting for request from provider(sender)
        channel.start_consuming()

    @staticmethod
    @try_except_decor
    @mongo_store
    def worker(**body):
        """
            Function which takes body of request from 'sender' and
                returns response from needed API request.
            The function that takes the request body from the "sender" and
                returns the required API request.

        :param body: encoded str - request string
        :return: (dict or list) - response to the required API request
        """

        print('-----------body-----------')
        print(body)
        print('-----------body-----------')

        action = body.pop('action')
        commit_hash = body.pop('hash')
        branch_name = body.pop('branch')
        if action == 'get_updated_all_commits':
            old_commits = body.pop('old_commits')

        with Builder(**body) as obj:
            methods = {
                # methods available for all git providers
                'get_repo': obj.get_repo,
                'get_branches': obj.get_branches,
                'get_commits': obj.get_commits,
                'get_commits_by_branch': obj.get_commits_by_branch,
                'get_commit_by_hash': obj.get_commit_by_hash,
                'get_contributors': obj.get_contributors,
                # methods available for Bitbucket only
                'get_updated_all_commits': obj.get_updated_all_commits if hasattr(obj, 'get_updated_all_commits') else None,
                'get_all_commits': obj.get_all_commits if hasattr(obj, 'get_all_commits') else None

            }
            if action == 'get_commit_by_hash':
                response = methods[action](commit_hash)
            elif action == 'get_commits_by_branch':
                response = methods[action](branch_name)
            elif action == 'get_updated_all_commits':
                response = methods[action](old_commits)
            else:
                response = methods[action]()
            print('------------response----------------')
            print(response)
            print('------------response----------------')

        return response

    @try_except_decor
    def callback(self, channel, method, props, body):
        """
            Consumes request from provider(sender)
        :param channel: unused param
        :param method: unused param
        :param props: unused param
        :param body: received message
        :return:
        """

        LOG.debug(f'[x] Received request: %s', body)

        # uses 'worker' function to get API response
        # and sends it to provider(sender)
        response = self.worker(body)

        # Sends the result back to the sender
        channel.basic_publish(exchange='',
                              routing_key=props.reply_to,
                              properties=pika.BasicProperties(correlation_id=props.correlation_id),
                              body=json.dumps(response))

        LOG.debug(f'[x] Sent response: %s', response)

        # used to tell the server that message was properly handled
        channel.basic_ack(delivery_tag=method.delivery_tag)
