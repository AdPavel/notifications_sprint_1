from django.conf import settings
from django.db.models.signals import post_save
from django.dispatch import receiver

from .models import User, Content, Template, Notification, Channel
from .utils import send_notification


@receiver(post_save, sender=User)
def send_welcome_email(
    instance: User, created: bool, **kwargs
) -> None:
    if created:
        content = Content.objects.get(id=settings.WELCOME_EMAIL_CONTENT_ID)
        confirm_url = f'{settings.CONFIRM_EMAIL_URL}?id={instance.id}&redirect_url={content.text["redirect_url"]}'
        email_content = Content.objects.create(
            name=f'Регистрация {instance.id}',
            text={'first_name': '', 'url': confirm_url}
        )

        template = Template.objects.get(id=settings.WELCOME_EMAIL_TEMPLATE_ID)
        channel = Channel.objects.get(name='email')
        priority = 'HIGH'

        notification = Notification.objects.create(
            content=email_content,
            template=template,
            channel=channel,
            priority=priority
        )
        notification.recipients.set([instance])

        try:
            send_notification(notification)
        except Exception:
            notification.status = 'OPEN'
            notification.save()
        else:
            notification.status = 'PROCESSED'
            notification.save()
