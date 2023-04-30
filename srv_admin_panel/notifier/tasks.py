import requests
from config.celery import app
from django.conf import settings

from .models import Notification, User, Content, Template, Channel
from .utils import send_notification


@app.task(bind=True)
def send_open_notifications(self):
    notifications = Notification.objects.filter(status='OPEN')
    for notification in notifications:
        try:
            send_notification(notification)
        except Exception as e:
            raise self.retry(exc=e, countdown=5)
        notification.status = 'PROCESSED'
        notification.save()


@app.task(bind=True)
def send_new_films_notifications(self):

    url = settings.NEW_MOVIES_URL
    response = requests.get(url, params={'amount': 10})
    response.raise_for_status()
    data = response.json()
    films = [film['title'] for film in data['films']]
    films_titles = ', '.join(films)

    recipients = User.objects.filter(is_subscribed=True, is_confirmed=True)
    content = Content.objects.create(
        name='Новые фильмы',
        text={'films': films_titles, 'first_name': '', 'unsubscribe_url': settings.UNSUBSCRIBE_URL}
    )
    template = Template.objects.get(id=settings.NEW_MOVIES_TEMPLATE_ID)
    channel = Channel.objects.get(name='email')
    priority = 'LOW'

    notification = Notification.objects.create(
        content=content,
        template=template,
        channel=channel,
        priority=priority
    )
    notification.recipients.set(recipients)

    try:
        send_notification(notification)
    except Exception as e:
        raise self.retry(exc=e, countdown=5)
    notification.status = 'PROCESSED'
    notification.save()
