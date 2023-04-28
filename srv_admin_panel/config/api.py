from ninja import NinjaAPI
from notifier.api import router as notifier_router
from ninja.security import HttpBearer
import os


class Auth(HttpBearer):
    def authenticate(self, request, token):
        if token == os.getenv('API_TOKEN'):
            return token


api = NinjaAPI(title='Notification service')

api.add_router('/notifier', notifier_router, tags=['notifier'], auth=Auth())
