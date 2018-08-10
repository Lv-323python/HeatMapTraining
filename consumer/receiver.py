"""
    Consumes requests from provider(sender), sends result to provider(sender)
"""
from ast import literal_eval

import pika
import json

from consumer.helper.builder import Builder  # pylint: disable=import-error
from consumer.helper.consumer_config import HOST, PORT, REQUEST_QUEUE, CALLBACK_QUEUE

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(
    host=HOST, port=PORT))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue=REQUEST_QUEUE)
CHANNEL.queue_declare(queue=CALLBACK_QUEUE)

print(' [*] Waiting for messages. To exit press CTRL+C')


def worker(body):
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


def callback(ch, method, props, body):
    """
        Consumes request from provider(sender)
    :param ch_c: unused param
    :param method_m: unused param
    :param properties_p: unused param
    :param body: received message
    :return:
    """

    # print unused params to pass pylit check
    print(ch, method, props)

    print(" [x] Received %r" % (body,))

    # uses 'worker' function to get API response
    # and send it to provider(sender)
    response = worker(body)

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=json.dumps(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


# declare consuming
CHANNEL.basic_consume(callback, queue=REQUEST_QUEUE, no_ack=True)

# start waiting for request from provider(sender)
CHANNEL.start_consuming()
