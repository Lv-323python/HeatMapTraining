'''
    qqqq
'''
from pprint import pprint
from ast import literal_eval

import pika


def sender(body):
    '''

    :param body:
    :return:
    '''

    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.17.0.2'))
    channel = connection.channel()

    channel.queue_declare(queue='request')
    channel.queue_declare(queue='response')

    channel.basic_publish(exchange='',
                          routing_key='request',
                          body=body)
    print(f" [x] Sent '{body}'")

    def callback(ch, method, properties, body):
        '''

        :param ch:
        :param method:
        :param properties:
        :param body:
        :return:
        '''

        print(" [x] Received %r\n" % (body,))
        result = literal_eval(body.decode())
        pprint(result)
        channel.stop_consuming()

    channel.basic_consume(callback,
                          queue='response',
                          no_ack=True)

    channel.start_consuming()
    connection.close()


EXAMPLE = "{'base_url':'https://api.bitbucket.org/2.0'," \
          "'version':'2','git_client':'bitbucket'," \
          "'token':None,'repo':'newtestrep','owner':" \
          " 'ihorss','hash':None,'branch':" \
          " None,'action': 'get_repo'}"

while True:
    MESSAGE = input(
        ' [*] Waiting for input. To exit press CTRL+C\nInput params\n '
        ' ex.{' + EXAMPLE + ':\n'
                            '      *optional - branch_name or hash_of_commit\nINPUT: ')
    sender(MESSAGE)
    print('Request has been executed\n\n')
