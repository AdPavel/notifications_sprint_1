from srv_worker.rabbitmq.reciver_rabbitmq import QueueConsumer
from srv_worker.rabbitmq.sender_rabbitmq import NotifierSender
from srv_admin_panel.config import settings


def send_notif(queue, template, user_first_name, user_email, content, priority):
    notifier = NotifierSender(rabbitmq_host=settings.rabbit_host, rabbitmq_queue_name=queue,
                              sendgrid_api_key=settings.sendgrid_api)
    notifier.start()

    context = {'username': user_first_name, 'text': content}
    notifier.notify(to=user_email, subject='Welcome', template=template, context=context,
                    priority=priority)


if __name__ == '__main__':

    for queue in settings.queue_names:
        consumer = QueueConsumer(rabbitmq_url='amqp://guest:guest@localhost:5672/', queue_name=queue)
        data = consumer.fetch_data()
        for user_id in data['users_id']:
            send_notif(queue=queue, template=data['template_id']['file'],
                       user_first_name=data['user_id']['first_name'],
                       user_email=data['user_id']['email'],
                       content=data['content_id']['text'],
                       priority=data['priority'])
