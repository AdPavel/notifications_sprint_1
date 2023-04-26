from pydantic import BaseSettings


class Settings(BaseSettings):
    sendgrid_api: str
    rabbit_host: str
    queue_names: list = list['email', 'sms', 'push']

    db_name: str = 'notifications_db'
    db_user: str = 'admin'
    db_password: str = 'admin'
    db_host: str = '127.0.0.1'
    db_port: int = 5432

settings = Settings()
