from typing import Union

from pydantic import BaseModel


class RabbitRecipient(BaseModel):

    email: str
    first_name: str


class RabbitNotification(BaseModel):

    notification_id: str
    recipients: list[RabbitRecipient]
    template: str
    content: Union[dict, None]
    subject: str
