from django.conf import settings

from .models import Notification
from .producer import RabbitPublisher
from .rabbit_models import RabbitRecipient, RabbitNotification


def convert_notification(notification: Notification) -> dict:
    recipients = [
        RabbitRecipient(email=recipient.email, first_name=recipient.first_name) for recipient in
        notification.recipients.all()
    ]
    rabbit_notification = RabbitNotification(
        notification_id=str(notification.id),
        recipients=recipients,
        template=notification.template.file.name,
        content=notification.content.text,
        subject=notification.template.name
    )
    print(rabbit_notification.dict())
    return rabbit_notification.dict()


def send_notification(notification: Notification):

    user = settings.RABBITMQ_DEFAULT_USER
    password = settings.RABBITMQ_DEFAULT_PASS
    host = settings.RABBIT_HOST
    port = settings.RABBIT_PORT

    connection_params = \
        f'amqp://{user}:{password}@{host}:{port}'
    publisher = RabbitPublisher(connection_params=connection_params, queue_name='email', max_priority=2)

    rabbit_notification = convert_notification(notification)

    priority = {
        'LOW': 0,
        'MEDIUM': 1,
        'HIGH': 2
    }

    publisher.publish(message=rabbit_notification, priority=priority[notification.priority])
