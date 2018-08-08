'''
    qqq
'''
from ast import literal_eval

import pika

from builder import Builder # pylint: disable=import-error


connection = pika.BlockingConnection(pika.ConnectionParameters(
    host='172.17.0.2'))
channel = connection.channel()

channel.queue_declare(queue='request')
channel.queue_declare(queue='response')

print(' [*] Waiting for messages. To exit press CTRL+C')


def worker(body):
    '''

    :param body:
    :return:
    '''

    body = literal_eval(body.decode())
    req_name = body['action']

    with Builder(body) as obj:

        request = {
            'get_repo': obj.get_repo,
            'get_branches': obj.get_branches,
            'get_commits': obj.get_commits,
            'get_commits_by_branch': obj.get_commits_by_branch,
            'get_commit_by_hash': obj.get_commit_by_hash,
            'get_contributors': obj.get_contributors
        }
        if not body['hash'] and not body['branch']:
            response = request[req_name]()
        elif not body['hash']:
            response = request[req_name](body['branch'])
        else:
            response = request[req_name](body['hash'])

        print('response', response)

        channel.basic_publish(exchange='',
                              routing_key='response',
                              body=str(response))
        return response

def callback(ch, method, properties, body):
    '''

    :param ch:
    :param method:
    :param properties:
    :param body:
    :return:
    '''

    print(" [x] Received body")
    worker(body)


channel.basic_consume(callback,
                      queue='request',
                      no_ack=True)

channel.start_consuming()
