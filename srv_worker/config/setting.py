from pydantic import BaseSettings


class Settings(BaseSettings):
    sendgrid_api: str
    rabbit_host: str
    queue_names: list = list['email', 'sms', 'push']

settings = Settings()
