import logging
import uuid

from django.http import HttpRequest
from django.shortcuts import redirect
from ninja import Router

from .api_models import UserSchema, Response
from .models import User, Notification, Template, Channel, Content
import os

router = Router()


@router.post('/create_user', response={200: Response, 400: Response})
def create_user(_request: HttpRequest, user: UserSchema):
    try:
        User.objects.create(
            id=user.id,
            first_name=user.first_name,
            last_name=user.last_name,
            email=user.email
        )
    except Exception as e:
        logging.exception(e)
        return 400, {'message': str(e)}
    else:
        return 200, {'message': 'Success'}


@router.get('/confirm_email', auth=None)
def confirm_email(_request: HttpRequest, id: uuid.UUID, redirect_url: str):
    try:
        user = User.objects.get(id=id)
        user.is_confirmed = True
        user.save()
    except Exception as e:
        logging.exception(e)
        return 400, {'message': str(e)}
    else:
        return redirect(redirect_url)


@router.get('/manage_subscription', auth=None)
def manage_subscription(_request: HttpRequest, id: uuid.UUID, subscribe: bool):
    try:
        user = User.objects.get(id=id)
        user.is_subscribed = subscribe
        user.save()
    except Exception as e:
        logging.exception(e)
        return 400, {'message': str(e)}
    else:
        return 200, {'message': 'Success'}


@router.get('/new_like')
def send_like_notification(_request: HttpRequest, id: uuid.UUID):
    try:
        user = User.objects.get(id=id)
        content = Content.objects.get(id=os.getenv('EVENT_CONTENT_ID'))
        template = Template.objects.get(id=os.getenv('EVENT_TEMPLATE_ID'))
        channel = Channel.objects.get(name='email')
        priority = 'LOW'
        status = 'OPEN'
        notification = Notification.objects.create(
            content=content,
            template=template,
            channel=channel,
            status=status,
            priority=priority
        )
        notification.recipients.set([user])
    except Exception as e:
        logging.exception(e)
        return 400, {'message': str(e)}
    else:
        return 200, {'message': 'Success'}
