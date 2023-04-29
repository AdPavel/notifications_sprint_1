from typing import Optional

import orjson
from pydantic import BaseModel


def orjson_dumps(v, *, default):
    # orjson.dumps возвращает bytes, а pydantic требует unicode, поэтому декодируем
    return orjson.dumps(v, default=default).decode()


class BaseOrjsonModel(BaseModel):
    class Config:
        # Заменяем стандартную работу с json на более быструю
        # json_encoders = {id: uuid4}
        json_loads = orjson.loads
        json_dumps = orjson_dumps
