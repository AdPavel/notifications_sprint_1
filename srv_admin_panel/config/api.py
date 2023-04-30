from django.conf import settings
from ninja import NinjaAPI
from ninja.security import HttpBearer
from notifier.api import router as notifier_router


class Auth(HttpBearer):
    def authenticate(self, request, token):
        if token == settings.API_TOKEN:
            return token


api = NinjaAPI(title='Notification service')

api.add_router('/notifier', notifier_router, tags=['notifier'], auth=Auth())
