import time

import pika
import json

from rabbitmq.reciver_rabbitmq import QueueConsumer
from rabbitmq.sender_rabbitmq import NotifierSender
from config.setting import settings


# def send_notif(queue, template, user_first_name, user_email, content, priority):
#     notifier = NotifierSender(rabbitmq_host=settings.rabbit_host, queue_name=queue,
#                               sendgrid_api_key=settings.sendgrid_api)
#     notifier.start()
#
#     context = {'username': user_first_name, 'text': content}
#     notifier.notify(to=user_email, subject='Welcome', template=template, context=context,
#                     priority=priority)
#
# ---------------- отпрвка
def connect_to_rabbit(connection_params, queue_name='email'):
    max_priority = 2

    # connect and get channel
    parameters = pika.URLParameters(connection_params)
    connection = pika.BlockingConnection(parameters)
    channel = connection.channel()
    # declare queue with max priority
    channel.queue_declare(
        queue=queue_name, arguments={"x-max-priority": max_priority}, durable=True
    )
    return channel


def publish(message, priority, channel, queue_name='email'):
    message = message
    channel.basic_publish(
        properties=pika.BasicProperties(priority=priority),
        exchange='',
        routing_key=queue_name,
        body=json.dumps(message)
    )


#  ----------------------------------------------------

if __name__ == '__main__':
    connection_params: str = \
        f'amqp://{settings.rabbitmq_default_user}:{settings.rabbitmq_default_pass}@{settings.rabbit_host}:{settings.rabbit_port}'
    queue_name = 'email'
    queue_to_send = 'email_to_send'
    # queues = {'queue_raw': 'email', 'queue_send': 'email_to_send'}

    # -------------------- отправка -----------------------
    chanel = connect_to_rabbit(connection_params)

    # for text, priority in ('{"id":"0", "text":"test0"}', 0), ('{"id":"1", "text":"test1"}', 1),\
    #         ('{"id":"2, "text":"test0"}',0), ('{"id":"3", "text":"test2"}', 2):
    #     publish(text, priority, chanel)

    text = {
        "notification_id": "e6491b80-def4-426c-b7e0-e1c935b48865",
        "recipients": [
            {
                "email": "adap2@mail.ru",
                "first_name": "lena",
            },
            {
                "email": "gmadap2@gmail.com",
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

    publish(text, 2, chanel)
    # ----------------------------------------------------

    notifier_sender = NotifierSender(connection_params=connection_params,
                                     queue_name=queue_name)

    # consumer = QueueConsumer(connection_params=connection_params,
    #                          queue_name=queue_name,
    #                          queue_send=queue_to_send,
    #                          max_priority=settings.max_priority)

    # consumer.start()
    notifier_sender.start()

    # while True:
    #     message = consumer.fetch_message()
    #     if message is not None:
    #         # Обратите внимание на паузу в 1 секунду между вызовами
    #         # fetch_message(), чтобы избежать загрузки процессора
    #         print(message)
    #     else:
    #         time.sleep(1)  # пауза в 1 секунду перед следующим вызовом fetch_message()

    # while True:
    #     for queue in settings.queue_names:
    #         consumer = QueueConsumer(
    #             connection_params=f'amqp://{settings.rabbitmq_default_user}:{settings.rabbitmq_default_pass}@{settings.rabbit_host}:{settings.rabbit_port}',
    #             queue_name=settings.queue)
    #         data = consumer.fetch_data()
    #         for user_id in data['users_id']:
    #             send_notif(queue=queue, template=data['template_id']['file'],
    #                        user_first_name=data['user_id']['first_name'],
    #                        user_email=data['user_id']['email'],
    #                        content=data['content_id']['text'],
    #                        priority=data['priority'])
