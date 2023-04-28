from rabbitmq.sender_rabbitmq import NotifierSender
from config.setting import settings


if __name__ == '__main__':
    connection_params: str = \
        f'amqp://{settings.rabbitmq_default_user}:{settings.rabbitmq_default_pass}@{settings.rabbit_host}:{settings.rabbit_port}'

    for queue_name in settings.queue_names:
        notifier_sender = NotifierSender(connection_params=connection_params,
                                         queue_name=queue_name)
        notifier_sender.start()

