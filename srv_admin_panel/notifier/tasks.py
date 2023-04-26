from config.celery import app
from notifier.models import Notification


def send_notification(notification):
    # Закинуть уведомление в очередь на отправку
    print(f'Уведомление {notification.id} отправлено!')


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
    # достаем из movies_api новые фильмы
    # получатели - все, кто подписан и подтвержден email
    # создаем notification
    # отправляем
    pass
