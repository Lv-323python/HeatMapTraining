import pika

HOST = 'localhost'
SEND_QUEUE_NAME = 'request'
RECEIVE_QUEUE_NAME = 'response'


def send(message):
    connection = pika.BlockingConnection(pika.ConnectionParameters(
            host=HOST))
    channel = connection.channel()
    
    channel.queue_declare(queue=SEND_QUEUE_NAME)
    
    channel.basic_publish(exchange='',
                          routing_key=SEND_QUEUE_NAME,
                          body=message)
    print(" [x] Sent message")
    connection.close()


def receive():
    connection = pika.BlockingConnection(pika.ConnectionParameters(
        host=HOST))
    channel = connection.channel()

    channel.queue_declare(queue=SEND_QUEUE_NAME)

    print(' [*] Waiting for messages. To exit press CTRL+C')

    def callback(ch, method, properties, body):
        print(" [x] Received %r" % (body,))

    channel.basic_consume(callback,
                          queue=SEND_QUEUE_NAME,
                          no_ack=True)

    channel.start_consuming()
