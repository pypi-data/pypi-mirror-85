from dataclasses import dataclass
from datetime import datetime
from typing import Dict

from . import Adapter
from .Fields.Intent import Intent
from .Fields.Message import Message
from .Fields.Record import Record
from .Fields.Slug import Slug
from .Fields.User import User


@dataclass
class FacebookAdapter(Adapter):

    def save(self, request: Dict, bot_answer: Message = None, intent: Intent = None, slug: Slug = None):
        if 'messaging' in request:
            request = request['messaging']

        record = Record(user=User(user_id=request['sender']['id']),
                        message=Message(text=request['message']['text'] if 'text' in request['message'] else ''),
                        intent=intent,
                        slug=slug,
                        payload=str(request),
                        timestamp=datetime.fromtimestamp(int(request['timestamp'] / 1000)),
                        sender='user')
        Adapter.save(self, record)

        record = Record(user=User(user_id=request['sender']['id']),
                        message=bot_answer,
                        intent=intent,
                        slug=slug,
                        payload=str(request),
                        timestamp=datetime.fromtimestamp(int(request['timestamp'] / 1000)),
                        sender='bot')
        Adapter.save(self, record)
