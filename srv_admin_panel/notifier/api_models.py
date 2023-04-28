from ninja import Schema, ModelSchema
from .models import User


class UserSchema(ModelSchema):
    class Config:
        model = User
        model_fields = ['id', 'email', 'first_name', 'last_name']


class Response(Schema):
    message: str
