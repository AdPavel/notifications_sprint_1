import queue

import pika
import json
import threading


class QueueConsumer:
    def __init__(self, rabbitmq_url, queue_name):
        self.rabbitmq_url = rabbitmq_url
        self.queue_name = queue_name

        self._connection = None
        self._channel = None
        self._consume_thread = None
        self._event = threading.Event()
        self._data_queue = queue.Queue()

    # Методы `_open_connection`, `_open_channel` и `_setup_queue` приватные,
    # он отвечает за открытие соединения, канала и создание очереди в RabbitMQ.
    # Этот код можно использовать в каждом методе, который работает с RabbitMQ, так что их не перебивает друг друга.
    def _open_connection(self):
        if self._connection is None or self._connection.is_closed:
            self._connection = pika.BlockingConnection(pika.URLParameters(self.rabbitmq_url))

    def _open_channel(self):
        self._open_connection()
        if self._channel is None or self._channel.is_closed:
            self._channel = self._connection.channel()

    def _setup_queue(self):
        self._open_channel()
        self._channel.queue_declare(queue=self.queue_name, durable=True)

    # Метод `_consume_messages` занимается получением сообщений из очереди,
    # сохранением их в очередь и установкой события `_event`, что сообщение было получено.
    def _consume_messages(self):
        self._open_channel()
        self._setup_queue()

        def callback(ch, method, properties, body):
            data = json.loads(body)
            self._data_queue.put(data)
            self._event.set()
            ch.basic_ack(delivery_tag=method.delivery_tag)

        self._channel.basic_consume(
            queue=self.queue_name,
            on_message_callback=callback)

        self._channel.start_consuming()

    # Метод `fetch_data` нужен для получения данных из очереди в место вызова.
    # Он запускает поток для получения данных, ждет подтверждения получения данных (`_event.wait()`),
    # загружает данные из очереди `_data_queue.get()` и очищает очередь
    # и выходит из функции, возвращая полученные данные.
    def fetch_data(self):
        self._consume_thread = threading.Thread(target=self._consume_messages)
        self._consume_thread.start()

        self._event.wait()
        self._event.clear()
        data = self._data_queue.get()
        self._data_queue.task_done()
        while not self._data_queue.empty():
            self._data_queue.get_nowait()
            self._data_queue.task_done()

        self._consume_thread.join()
        return data
