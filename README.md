# Сервис отправки уведомлений онлайн-кинотеатра
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
2. Создайте файл `.env` и заполните его аналогично `.env.example`
3. Активируйте виртуальное окружение и установите зависимости
```
. .venv/bin/activate
pip install -r app/requirements.txt
```
4. Примените миграции и создайте супер пользователя
```
python app/manage.py migrate
python app/manage.py createsuperuser
```
5. Запустите сервис
```
python app/manage.py runserver
```
Сервис будет доступен по адресу http://127.0.0.1:8000/

Админка http://127.0.0.1:8000/admin
