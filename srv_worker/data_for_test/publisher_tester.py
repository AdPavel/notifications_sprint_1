import pika
import json

from config.setting import settings


class RabbitPublisher:
    def __init__(self, connection_params: str, queue_name: str, max_priority: int):
        self.connection_params = connection_params
        self.queue_name = queue_name
        self.max_priority = max_priority

    def connect_to_rabbit(self):
        parameters = pika.URLParameters(self.connection_params)
        connection = pika.BlockingConnection(parameters)
        channel = connection.channel()
        channel.queue_declare(
            queue=self.queue_name,
            arguments={'x-max-priority': self.max_priority},
            durable=True
        )
        return channel

    def publish(self, message: dict, priority: int, channel: object):
        message = message
        channel.basic_publish(
            properties=pika.BasicProperties(priority=priority),
            exchange='',
            routing_key=self.queue_name,
            body=json.dumps(message)
        )


text = {
    "notification_id": "e6491b80-def4-426c-b7e0-e1c935b48865",
    "recipients": [
        {
            "email": "test@mail.ru",
            "first_name": "lena",
        },
        {
            "email": "test@gmail.com",
            "first_name": "lena",
        }
    ],
    "template": "welcome.html",
    "content": {
        "name": "",
        "field_1": "value",
        "field_2": "value",
    },
    "subject": "template_name"
}

if __name__ == '__main__':
    connection_params = \
        f'amqp://{settings.rabbitmq_default_user}:{settings.rabbitmq_default_pass}@{settings.rabbit_host}:{settings.rabbit_port}'
    publisher = RabbitPublisher(connection_params=connection_params, queue_name='email', max_priority=2)
    chanel = publisher.connect_to_rabbit()
    for priority in range(3):
        publisher.publish(message=text, priority=priority, channel=chanel)
