import json
import pathlib
import smtplib
import sys
from email.message import EmailMessage

import jinja2
import pika

sys.path.append("..")

from config.setting import settings
from db.postgres import PostgresDB

pg_db = PostgresDB(host=settings.postgres_host, port=settings.postgres_port,
                   database=settings.postgres_db, user=settings.postgres_user,
                   password=settings.postgres_password)


class NotifierSender:
    def __init__(self, connection_params: str, queue_name: str):
        self.connection_params = connection_params
        self.queue_name = queue_name
        self.server = smtplib.SMTP_SSL('smtp.gmail.com', 465)

        env_template = f"{pathlib.Path(__file__).resolve().parent.parent}/media/"
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(env_template))

    def start(self):
        connection = pika.BlockingConnection(pika.URLParameters(self.connection_params))
        channel = connection.channel()

        channel.queue_declare(queue=self.queue_name, arguments={'x-max-priority': settings.max_priority},
                              durable=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=False)

        print(f' [*] Waiting for messages from {self.queue_name}')
        channel.start_consuming()

    def send_email(self, email: str, _id: str, message: EmailMessage):

        self.server.login(settings.email, settings.email_password)
        try:
            self.server.sendmail(settings.email, email, message.as_string())
            data = {'status': 'CLOSED'}
            pg_db.update_data(table_name='notifier_notification', _id=_id, data=data)
            print('Send email: SUCCESS')
        except Exception as ex:
            print('Error sending email:', ex)
            # отправить в PG с приоритетом low и статус open
            data = {'status': 'OPEN', 'priority': 'LOW'}
            pg_db.update_data(table_name='notifier_notification', _id=_id, data=data)

    def callback(self, channel, method, properties, body):
        if body is not None:
            message = json.loads(body.decode('utf-8'))
            notification_id = message['notification_id']
            subject = message['subject']
            template = self.jinja_env.get_template(message['template'])
            content = message['content']
            recipients = message['recipients']
            for recipient in recipients:
                email, first_name = recipient.values()
                content['first_name'] = first_name
                html_content = template.render(**content)

                message = EmailMessage()
                message['From'] = settings.email
                message["To"] = email
                message["Subject"] = subject

                message.add_alternative(html_content, subtype='html')

                self.send_email(email=email, _id=notification_id, message=message)

        channel.basic_ack(delivery_tag=method.delivery_tag)
