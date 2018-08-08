"""
    Sends request, waits for response, returns response
"""

import pika


def sender(body):
    """

    :param body: str - string of params for request
    :return response: str - response from consumer
    """

    # declare result
    list_for_result = []

    # start connection
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host='172.17.0.2'))
    channel = connection.channel()

    # declare queues
    channel.queue_declare(queue='request')
    channel.queue_declare(queue='response')

    # sends message to consumer
    channel.basic_publish(exchange='', routing_key='request', body=body)

    def callback(a_a, b_b, c_c, body):
        """
            Base function for consuming
        :param a_a: unused param
        :param b_b: unused param
        :param c_c: unused param
        :param body: received message
        :return: None, but save response from consumer to 'result'
        """
        # print unused params to pass pylit check
        print(a_a, b_b, c_c)

        print(" [x] Received %r\n" % (body,))

        # stops waiting for response
        channel.stop_consuming()

        # save response from consumer to 'result'
        list_for_result.append(body)

    # declare consuming params
    channel.basic_consume(callback, queue='response', no_ack=True)

    # starts consuming(waiting for) response using 'callback' function
    channel.start_consuming()
    connection.close()

    # gets response from list_for_result and clears list_for_result
    result = list_for_result[0]
    list_for_result.clear()
    # returns result
    return result


# # Working example request message for bitbucket
#
# EXAMPLE = "{'base_url':'https://api.bitbucket.org/2.0'," \
#           "'version':'2','git_client':'bitbucket'," \
#           "'token':None,'repo':'newtestrep','owner':" \
#           " 'ihorss','hash':None,'branch':" \
#           " None,'action': 'get_repo'}"
#
# # for test without flask web server
# from pprint import pprint
# from ast import literal_eval
#
# while True:
#     MESSAGE = input(
#         ' [*] Waiting for input. To exit press CTRL+C\nInput params\n '
#         ' ex.:\n   ' + EXAMPLE + '\n\nINPUT:\n ')
#     response = sender(MESSAGE)
#     pprint(literal_eval(response.decode()))
#     print('Request has been executed\n\n')
