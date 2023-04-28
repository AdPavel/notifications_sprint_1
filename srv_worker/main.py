from rabbitmq.sender_rabbitmq import NotifierSender
from config.setting import settings


if __name__ == '__main__':

    user = settings.rabbitmq_default_user
    password = settings.rabbitmq_default_pass
    host = settings.rabbit_host
    port = settings.rabbit_port

    connection_params: str = f'amqp://{user}:{password}@{host}:{port}'

    for queue_name in settings.queue_names:
        notifier_sender = NotifierSender(connection_params=connection_params,
                                         queue_name=queue_name)
        notifier_sender.start()

