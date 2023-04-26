import pika
import json
from sendgrid import SendGridAPIClient
from sendgrid.helpers.mail import Email
import jinja2

from ..config.setting import settings
from ..db.postgres import PostgresDB

pg_db = PostgresDB(host=settings.db_host, port=settings.db_port,
                   database=settings.db_name, user=settings.db_user, password=settings.db_password)


class NotifierSender:
    def __int__(self, rabbitmq_host: str, rabbitmq_queue_name: str, sendgrid_api_key: str):
        self.rabbitmq_host = rabbitmq_host
        self.rabbitmq_queue_name = rabbitmq_queue_name
        self.sendgrid_client = SendGridAPIClient(api_key=sendgrid_api_key)


        # настройка окружения для шаблонизации Jinja
        self.jinja_env = jinja2.Environment(loader=jinja2.FileSystemLoader('templates'))

    def start(self):
        connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_host))
        channel = connection.channel()

        channel.queue_declare(queue=self.rabbitmq_queue_name, durable=True)

        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.rabbitmq_queue_name, on_message_callback=self.callback, auto_ack=False)

        print(' [*] Waiting for messages.')
        channel.start_consuming()

    def callback(self, channel, method, properties, body):
        message = json.loads(body)

        # загрузка шаблона и рендеринг содержимого HTML-письма
        template = self.jinja_env.get_template(message['template'])
        html_content = template.render(**message['context'])

        email = Email(
            to=message['to'],
            subject=message['subject'],
            html_content=html_content)

        try:
            for i in range(3):
                response = self.sendgrid_client.send(email)
                if response.status_code == 200 or response.status_code == 202:
                    print('Email sent successfully')
                    # отправить в PG с приоритетом low и статус closed
                    pg_db.update_data(table_name='notification', _id=message['id'], )
                    break
                else:
                    print('Error sending email, retrying...')
        except Exception as ex:
            print('Error sending email:', ex)
            # отправить в PG с приоритетом low и статус open
        finally:
            channel.basic_ack(delivery_tag=method.delivery_tag)

    def notify(self, to, subject, template, context, priority):
        message = {
            'to': to,
            'subject': subject,
            'template': template,
            'context': context
        }

        priority_levels = {'low': 0, 'medium': 1, 'high': 2}
        priority_level = min(priority_levels[priority], 2)
        # установка приоритетов

        properties = pika.BasicProperties(delivery_mode=2, priority=priority_level)

        connection = pika.BlockingConnection(pika.ConnectionParameters(self.rabbitmq_host))
        channel = connection.channel()

        channel.queue_declare(queue=self.rabbitmq_queue_name, durable=True)
        channel.basic_publish(exchange='', routing_key=self.rabbitmq_queue_name, body=json.dumps(message),
                              properties=properties)

        print('Message sent to queue:', priority)

        connection.close()
