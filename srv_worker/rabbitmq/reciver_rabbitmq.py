import json
import pika


class QueueConsumer:
    def __init__(self, connection_params: str, queue_name: str, queue_send: str ,max_priority):
        self.connection_params = connection_params
        self.queue_name = queue_name
        self.queue_send = queue_send
        self.max_priority = max_priority

    ''''
    Метод забирает из очереди не обработаные данные готовит их для письма и кладет в очередь на отправку 
    '''
    def send_notify(self, to: str, subject: str, template: str, content: str, _id, priority: int):
        message = {
            'to': to,
            'subject': subject,
            'template': template,
            'context': content,
            '_id': _id
        }

        connection = pika.BlockingConnection(pika.URLParameters(self.connection_params))
        channel = connection.channel()
        channel.queue_declare(queue=self.queue_send,
                              arguments={"x-max-priority": self.max_priority},
                              durable=True)

        channel.basic_publish(
                    properties=pika.BasicProperties(priority=priority),
                    exchange='',
                    routing_key=self.queue_send,
                    body=json.dumps(message)
                )

        print('Message sent to queue:', priority)

        connection.close()

    def callback(self, channel, method, properties, body):
        if body is not None:
            message = json.loads(body.decode('utf-8'))
            notification_id = message['notification_id']
            subject = message['subject']
            template = message['template']
            content = message['content']
            recipients = message['recipients']
            for recipient in recipients:
                email, first_name = recipient.values()
                content['name'] = first_name
                self.send_notify(to=email, subject=subject,
                                 template=template, content=content,
                                 _id=notification_id, priority=properties.priority)

    def start(self):
        connection = pika.BlockingConnection(pika.URLParameters(self.connection_params))
        channel = connection.channel()

        channel.queue_declare(queue=self.queue_name, arguments={'x-max-priority': 2}, durable=True)
        channel.basic_qos(prefetch_count=1)
        channel.basic_consume(queue=self.queue_name, on_message_callback=self.callback, auto_ack=True)

        channel.start_consuming()
