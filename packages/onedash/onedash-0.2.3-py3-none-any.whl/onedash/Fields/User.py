from dataclasses import dataclass
from typing import Union


@dataclass
class User:
    user_id: Union[str, int]
