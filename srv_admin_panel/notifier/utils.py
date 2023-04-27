from .models import Notification
from .rabbit_models import RabbitRecipient, RabbitNotification


def convert_notification(notification: Notification) -> dict:
    recipients = [
        RabbitRecipient(email=recipient.email, first_name=recipient.first_name) for recipient in
        notification.recipients.all()
    ]
    rabbit_notification = RabbitNotification(
        id=str(notification.id),
        recipients=recipients,
        template=notification.template.file.path,
        content=notification.content.text,
        subject=notification.template.name
    )
    print(rabbit_notification.dict())
    return rabbit_notification.dict()
