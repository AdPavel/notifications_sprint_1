from datetime import datetime, timezone
import pathlib

import pika
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Mail
import jinja2

import sys

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
        self.sendgrid_client = SendGridAPIClient(api_key=settings.sendgrid_api)

        env_template = f"{pathlib.Path(__file__).resolve().parent.parent}/media/"
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader(env_template))

    def start(self):
        connection = pika.BlockingConnection(pika.URLParameters(self.connection_params))
        channel = connection.channel()

        channel.queue_declare(queue=self.queue_name, arguments={"x-max-priority": settings.max_priority},
                              durable=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=False)

        print(f' [*] Waiting for messages from {self.queue_name}')
        channel.start_consuming()

    def send_email(self, email, _id):
        try:
            for i in range(3):
                response = self.sendgrid_client.send(email)
                if response.status_code == 200 or response.status_code == 202:
                    print('Email sent successfully')
                    # отправить в PG с текущей датой и статусом closed
                    data = {'status': 'CLOSED'}
                    pg_db.update_data(table_name='notifier_notification', _id=_id, data=data)
                    break
                else:
                    print('Error sending email, retrying...')
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

                email = Mail(
                    from_email=settings.email,
                    to_emails=email,
                    subject=subject,
                    html_content=html_content)

                self.send_email(email=email, _id=notification_id)

        channel.basic_ack(delivery_tag=method.delivery_tag)
