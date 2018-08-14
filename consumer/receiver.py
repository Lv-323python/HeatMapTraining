"""
    Module that starts receiving requests from 'sender' and
     sends responses back to the last one
"""

from rabbitmq_receiver import RabbitMQReceiver

RABBITMQ_RECEIVER = RabbitMQReceiver()
