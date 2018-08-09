# import pika
#
# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=8080))
#
# channel = connection.channel()
#
# channel.queue_declare(queue='request')
# channel.queue_declare(queue='response')
#
#
# def on_request(ch, method, props, body):
#     response = body
#     print(response)
#     ch.basic_publish(exchange='',
#                      routing_key='response',
#                      properties=pika.BasicProperties(correlation_id=props.correlation_id),
#                      body=str(response))
#     ch.basic_ack(delivery_tag=method.delivery_tag)
#
#
# channel.basic_consume(on_request, queue='request')
#
# print(" [x] Awaiting RPC requests")
# channel.start_consuming()
import pika
import pika.exceptions
import json
import time
# from server_config import HOST, PORT, RPC_QUEUE, REQUEST_SENDER_CHOICES
from heat_map_training.request_sender.bitbucket_request_sender import BitbucketRequestSender
from heat_map_training.request_sender.github_request_sender import GithubRequestSender
from heat_map_training.request_sender.gitlab_request_sender import GitLabRequestSender


def on_request(ch, method, props, body):
    message = body
    print('-----------------received message--------------')
    print(message)
    print('-----------------------------------------------')
    request_sender = None

    # if message['git_client'] == 'bitbucket_request_sender':
    #     request_sender = BitbucketRequestSender(
    #         repo=message['repository_name'],
    #         owner=message['owner_username']
    #     )
    # elif message['git_client'] == 'gitlab_request_sender':
    #     request_sender = GitLabRequestSender(
    #         repo=message['repository_name'],
    #         owner=message['owner_username']
    #     )
    # else:
    #     request_sender = GithubRequestSender(
    #         repo=message['repository_name'],
    #         owner=message['owner_username']
    #     )

    print('Processing response...')
    # response = request_sender.get_repo()
    response = message
    print('Response is processed!')
    print('--------------------response-------------------')
    print(response)
    print('-----------------------------------------------')
    print('Sending response back...')

    ch.basic_publish(exchange='',
                     routing_key=props.reply_to,
                     properties=pika.BasicProperties(correlation_id=props.correlation_id),
                     body=response.decode())
    ch.basic_ack(delivery_tag=method.delivery_tag)


print('Connecting to rabbitmg...')
RETRIES=30
while True:
    try:
        connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=8080))
        channel = connection.channel()
        break
    except pika.exceptions.ConnectionClosed as exc:
        if RETRIES == 0:
            print('Failed to connect!')
            raise exc
        RETRIES -= 1
        time.sleep(1)
print('Successfully connected!')

# connection = pika.BlockingConnection(pika.ConnectionParameters(host='localhost', port=8080))
# channel = connection.channel()

channel.queue_declare(queue='request')
channel.basic_qos(prefetch_count=1)
channel.basic_consume(on_request, queue='request')

print(" [x] Awaiting RPC requests")
channel.start_consuming()