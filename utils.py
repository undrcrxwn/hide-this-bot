from enum import Enum
from aiogram import types

class BaseEnum(Enum):
    @staticmethod
    def parse_key(full_name: Enum):
        return str(full_name).split('.')[-1]

class PostMode(BaseEnum):
    SPOILER = 0
    FOR = 1
    EXCEPT = 2

def get_formatted_username_or_id(user: types.User):
    return 'id' + str(user.id) if user.username is None else '@' + user.username
