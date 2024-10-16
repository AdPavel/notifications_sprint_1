# Сервис отправки уведомлений онлайн-кинотеатра

Ссылка на репозиторий: https://github.com/AdPavel/notifications_sprint_1

Ссылка на схему: https://miro.com/app/board/uXjVMStUUjk=/?share_link_id=383027605319

## Установка
### Как установить через контейнер
1. Поднимите контейнер
```
docker-compose up -d --build
```
2. Если нужно, создайте суперпользователя
```
docker-compose exec admin python manage.py createsuperuser
```

Админка http://localhost/admin

Админка RabbitMQ: http://localhost:15672/ ``` login: admin, pass: admin ```

Админка MailHog: http://localhost:8025

Документация к API http://localhost/api/docs

### Как установить локально
1. Поднимите postgres
```
docker run -d \
  --name notifications_postgres \
  -p 5432:5432 \
  -e POSTGRES_PASSWORD=admin \
  -e POSTGRES_USER=admin \
  -e POSTGRES_DB=notifications_db  \
  postgres
```
2. Поднимите redis
```
docker run -d -p 6379:6379 redis
```
3. Создайте файл `.env` и заполните его аналогично `.env.example`
4. Активируйте виртуальное окружение и установите зависимости
```
. .venv/bin/activate
pip install -r app/requirements.txt
```
5. Примените миграции и создайте супер пользователя
```
python app/manage.py migrate
python app/manage.py createsuperuser
```
6. Запустите сервис
```
python srv_admin_panel/manage.py runserver
```
7. Поднимите celery
```
cd srv_admin_panel/
celery -A config worker --beat --scheduler django --loglevel=info
```

Сервис будет доступен по адресу http://127.0.0.1:8080/

Админка http://127.0.0.1:8080/admin

## Как использовать

Чтобы настроить отправку писем с подтверждением регистрации нужно:
1. Через админку создать шаблон, записать его id в WELCOME_EMAIL_TEMPLATE_ID
2. Через админку создать контент, записать его id в WELCOME_EMAIL_CONTENT_ID
3. Заполнить значение переменной CONFIRM_EMAIL_URL
4. Поместить в поле "Текст" контента значение формата {"redirect_url": "https://google.com"}
5. Через админку создать канал email

Чтобы настроить рассылку писем с новинками, нужно:
1. Через админку создать шаблон, записать его id в NEW_MOVIES_TEMPLATE_ID
2. Заполнить значение переменной NEW_MOVIES_URL
3. В таблице "Периодические задачи" создать новый объект, в поле "Задачи (зарегистрированные)" выбрать `notifier.tasks.send_new_films_notifications`, настроить расписание
4. Через админку создать канал email

Чтобы настроить рассылку неотправленных писем, нужно:
1. В таблице "Периодические задачи" создать новый объект, в поле "Задачи (зарегистрированные)" выбрать `notifier.tasks.send_open_notifications`, настроить расписание
2. Через админку создать канал email
3. Таск будет собирать уведомления со статусом "Ждет отправки" и ставить их в очередь на отправку

Чтобы отправить свое уведомление, нужно:
1. Создать объект в таблице "Уведомления"
2. Выбрать уведомление и в поле "Действия" выбрать "Отправить"
3. Через админку создать канал email
4. Если вы хотите, чтобы в уведомлении содержалось имя получателя добавьте в контент должен содержать {"first_name": ""}
