import time

import pika

from rabbitmq.reciver_rabbitmq import QueueConsumer
from rabbitmq.sender_rabbitmq import NotifierSender
from config.setting import settings


def send_notif(queue, template, user_first_name, user_email, content, priority):
    notifier = NotifierSender(rabbitmq_host=settings.rabbit_host, rabbitmq_queue_name=queue,
                              sendgrid_api_key=settings.sendgrid_api)
    notifier.start()

    context = {'username': user_first_name, 'text': content}
    notifier.notify(to=user_email, subject='Welcome', template=template, context=context,
                    priority=priority)

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
    message = message + str(priority)
    channel.basic_publish(
        properties=pika.BasicProperties(priority=priority),
        exchange='',
        routing_key=queue_name,
        body=message
    )
#  ----------------------------------------------------

if __name__ == '__main__':

    connection_params = f'amqp://{settings.rabbitmq_default_user}:{settings.rabbitmq_default_pass}@{settings.rabbit_host}:{settings.rabbit_port}'
    queue_prefix = 'email'

#-------------------- отправка -----------------------
    chanel = connect_to_rabbit(connection_params)

    for text, priority in ('test0', 0), ('test1', 1), ('test2',0), ('test3', 2):
        publish(text, priority, chanel)
#----------------------------------------------------

    consumer = QueueConsumer(connection_params, queue_prefix)

    message = consumer.consume()
    print(message)

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
    #             queue_prefix=settings.queue)
    #         data = consumer.fetch_data()
    #         for user_id in data['users_id']:
    #             send_notif(queue=queue, template=data['template_id']['file'],
    #                        user_first_name=data['user_id']['first_name'],
    #                        user_email=data['user_id']['email'],
    #                        content=data['content_id']['text'],
    #                        priority=data['priority'])
