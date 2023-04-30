import json

import pika


class RabbitPublisher:
    def __init__(self, connection_params, queue_name, max_priority):
        self.connection_params = connection_params
        self.queue_name = queue_name
        self.max_priority = max_priority

    def publish(self, message, priority):

        parameters = pika.URLParameters(self.connection_params)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(
            queue=self.queue_name,
            arguments={'x-max-priority': self.max_priority},
            durable=True
        )
        channel.basic_publish(
            properties=pika.BasicProperties(priority=priority),
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message)
        )
        connection.close()
