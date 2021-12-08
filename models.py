import os
from datetime import datetime

from aiogram import types
from loguru import logger
from peewee import Model, BigIntegerField, IntegerField, CharField, BooleanField, TimestampField, ForeignKeyField
from playhouse.db_url import connect

from utils import get_formatted_username_or_id, PostMode

db = connect(os.environ['DATABASE_URL'])

class BaseModel(Model):
    class Meta:
        database = db

class User(BaseModel):
    user_id = BigIntegerField(primary_key = True)
    username = CharField(null = True)
    first_name = CharField()
    last_name = CharField(null = True)
    language_code = CharField(null = True)
    has_dialog = BooleanField()
    inline_queries_count = IntegerField()
    first_interaction_time = TimestampField()
    last_interaction_time = TimestampField()

    @staticmethod
    def get_or_create(user: types.User):
        try:
            result = User.get_by_id(user.id)
            result.refresh(user)
        except Exception as e:
            result = User.create(
                user_id = user.id,
                first_name = user.first_name,
                last_name = user.last_name,
                username = user.username,
                language_code = user.language_code,
                has_dialog = False,
                inline_queries_count = 0,
                first_interaction_time = datetime.utcnow(),
                last_interaction_time = datetime.utcnow())
            logger.info('new user ' + get_formatted_username_or_id(user) + ' has been saved to the database')
        return result

    def refresh(self, user: types.User):
        self.username = user.username
        self.first_name = user.first_name
        self.last_name = user.last_name
        self.language_code = user.language_code
        self.last_interaction_time = datetime.utcnow()
        self.save()

    def get_values(self):
        return (
            self.user_id,
            self.username,
            self.language_code,
            self.has_dialog,
            self.inline_queries_count,
            self.first_interaction_time,
            self.last_interaction_time)

class Post(BaseModel):
    author = ForeignKeyField(User)
    content = CharField()
    scope = CharField()
    creation_time = TimestampField()

    def get_scope_mentions(self):
        return str(self.scope).lower().split(' ')

    def set_scope_mentions(self, mentions: set):
        self.scope = ' '.join(mentions).replace('@', '')
        self.save()

    def update_scope_mention(self, old_mention: str, new_mention: str):
        mentions = self.get_scope_mentions()
        mentions.remove(old_mention.lower())
        mentions.append(new_mention.lower())
        self.set_scope_mentions(set(mentions))

    def can_be_accessed_by(self, user: types.User, mode: PostMode):
        access_granted = False
        if mode == PostMode.SPOILER:
            access_granted = True
        elif mode == PostMode.FOR:
            if user.username and user.username.lower() in self.get_scope_mentions():
                access_granted = True
                self.update_scope_mention(user.username, str(user.id))
            else:
                access_granted = user.id == self.author.user_id or str(user.id) in self.scope
        elif mode == PostMode.EXCEPT:
            if user.username and user.username.lower() in self.get_scope_mentions():
                access_granted = False
                self.update_scope_mention(user.username, str(user.id))
            else:
                access_granted = str(user.id) not in self.scope
        return access_granted

db.create_tables([User, Post], safe = True)
