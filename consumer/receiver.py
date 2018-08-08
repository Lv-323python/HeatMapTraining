"""
    Consumes requests from provider(sender), sends result to provider(sender)
"""
from ast import literal_eval

import pika

from helper.builder import Builder  # pylint: disable=import-error

CONNECTION = pika.BlockingConnection(pika.ConnectionParameters(
    host='172.17.0.2'))
CHANNEL = CONNECTION.channel()

CHANNEL.queue_declare(queue='request')
CHANNEL.queue_declare(queue='response')

print(' [*] Waiting for messages. To exit press CTRL+C')


def worker(body):
    """

    :param body:
    :return: None, but sends result to provider(sender)
    """
    # decode request from provider(sender)
    body = literal_eval(body.decode())
    req_name = body['action']
    print('body in worker', body)

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
        if body['hash'] is None and body['branch'] is None:
            response = request[req_name]()
        elif body['hash'] is None:
            response = request[req_name](body['branch'])
        else:
            response = request[req_name](body['hash'])

        print('response', response)

        # sends API response to provider(sender)
        CHANNEL.basic_publish(exchange='',
                              routing_key='response',
                              body=str(response))


def callback(ch_c, method_m, properties_p, body):
    """
        Consumes request from provider(sender)
    :param ch_c: unused param
    :param method_m: unused param
    :param properties_p: unused param
    :param body: received message
    :return:
    """

    # print unused params to pass pylit check
    print(ch_c, method_m, properties_p)

    print(" [x] Received %r" % (body,))

    # uses 'worker' function to get API response
    # and send it to provider(sender)
    worker(body)


# declare consuming
CHANNEL.basic_consume(callback, queue='request', no_ack=True)

# start waiting for request from provider(sender)
CHANNEL.start_consuming()
