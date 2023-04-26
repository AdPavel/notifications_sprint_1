# Сервис отправки уведомлений онлайн-кинотеатра
## Как установить через контейнер
1. Поднимите контейнер
```
docker-compose up -d --build
```
2. Если нужно, создайте суперпользователя
```
docker-compose exec admin python manage.py createsuperuser
```
## Как установить локально
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

Сервис будет доступен по адресу http://127.0.0.1:8000/

Админка http://127.0.0.1:8000/admin
