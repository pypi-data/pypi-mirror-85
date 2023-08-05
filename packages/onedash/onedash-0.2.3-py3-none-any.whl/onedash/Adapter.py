from dataclasses import dataclass

import requests

from .Fields.Record import Record
from .config import insert_record_url


@dataclass
class Adapter:
    token: str
    remove_pii: bool = True

    def save(self, record: Record):
        payload = {'user_id': record.user.user_id,
                   'message': record.message.text if record.message is not None else '',
                   'intent_name': record.intent.name if record.intent is not None else '',
                   'payload': record.payload if record.payload is not None else '',
                   'timestamp': str(record.timestamp),
                   'slug': record.slug.name if record.slug is not None else '',
                   'message_tag': [],
                   'sender': record.sender,
                   'channel': record.channel if record.channel is not None else '',
                   'version': 2,
                   'remove_pii': self.remove_pii}
        if record.intent is not None:
            payload['message_tag'] = record.intent.list_of_properties()
        if record.reference:
            payload.update(record.reference.json())
        headers = {'Authorization': self.token}
        response = requests.post(url=insert_record_url, headers=headers, json=payload)
        return response
