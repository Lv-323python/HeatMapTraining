import pika

connection = pika.BlockingConnection(pika.ConnectionParameters(host='172.17.0.4'))

channel = connection.channel()

channel.queue_declare(queue='request')
channel.queue_declare(queue='response')


def on_request(ch, method, props, body):
    response = body
    print(response)
    ch.basic_publish(exchange='',
                     routing_key='response',
                     body=str(response))
    ch.basic_ack(delivery_tag=method.delivery_tag)


channel.basic_consume(on_request, queue='request')

print(" [x] Awaiting RPC requests")
channel.start_consuming()
