from config.celery import app
from .models import Notification, User, Content, Template, Channel
from .utils import convert_notification
import requests
import os


def send_notification(notification):
    # Закинуть уведомление в очередь на отправку
    print(notification)


@app.task(bind=True)
def send_open_notifications(self):
    notifications = Notification.objects.filter(status='OPEN')
    for notification in notifications:
        rabbit_notification = convert_notification(notification)
        try:
            send_notification(rabbit_notification)
        except Exception as e:
            raise self.retry(exc=e, countdown=5)
        notification.status = 'PROCESSED'
        notification.save()


@app.task(bind=True)
def send_new_films_notifications(self):

    url = os.getenv('NEW_MOVIES_URL')
    response = requests.get(url, params={'amount': 10})
    response.raise_for_status()
    data = response.json()
    films = [film['title'] for film in data['films']]
    films_titles = ', '.join(films)

    recipients = User.objects.filter(is_subscribed=True, is_confirmed=True)
    content = Content.objects.create(
        name='Новые фильмы',
        text={"films": films_titles}
    )
    template = Template.objects.get(id=os.getenv('NEW_MOVIES_TEMPLATE_ID'))
    channel = Channel.objects.get(name='email')
    priority = 'LOW'

    notification = Notification.objects.create(
        content=content,
        template=template,
        channel=channel,
        priority=priority
    )
    notification.recipients.set(recipients)

    rabbit_notification = convert_notification(notification)
    try:
        send_notification(rabbit_notification)
    except Exception as e:
        raise self.retry(exc=e, countdown=5)
    notification.status = 'PROCESSED'
    notification.save()
