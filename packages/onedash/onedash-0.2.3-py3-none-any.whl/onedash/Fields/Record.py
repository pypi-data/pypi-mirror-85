from datetime import datetime
from dataclasses import dataclass
from . import (Intent, Slug, Message, Reference, User)


@dataclass
class Record:
    user: User
    message: Message = None
    reference: Reference = None
    intent: Intent = None
    slug: Slug = None
    payload: str = None
    timestamp: datetime = None
    channel: str = None
    sender: str = None

    def __post_init__(self):
        if self.message is None and not (self.intent is not None and self.intent.is_non_text_intent):
            raise ValueError('Message should be not empty')
        if self.sender is None:
            raise ValueError('Sender should be not empty')
        if self.timestamp is None:
            self.timestamp = datetime.now().replace(microsecond=0)
