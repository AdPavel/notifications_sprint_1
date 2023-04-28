import pathlib
from pydantic import BaseSettings


class Settings(BaseSettings):
    rabbit_host: str
    rabbit_port: int
    rabbitmq_default_user: str
    rabbitmq_default_pass: str
    queue_names: list[str]
    max_priority: int

    postgres_db: str
    postgres_user: str
    postgres_password: str
    postgres_host: str
    postgres_port: int

    email: str
    email_password: str

    class Config:

        env_file = f"{pathlib.Path(__file__).resolve().parent.parent.parent}/.env"
        env_file_encoding = 'utf-8'


settings = Settings()
