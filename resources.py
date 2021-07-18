from aiogram import types
import random
from locales_dict import *

class QueryResults:
    def __init__(self, locales: LocalesDict):
        self.locales = locales

    def message_too_long(self, lang: str):
        message_content = types.InputTextMessageContent(self.locales[lang].message_too_long_message)
        return types.InlineQueryResultArticle(
            id = '1', title = self.locales[lang].message_too_long_title,
            input_message_content = message_content,
            description = self.locales[lang].message_too_long_description,
            thumb_url = 'https://i.imgur.com/xblMvAx.png')

    def mode_for(self, lang: str, post_id, body, scope_string):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard =
            [[types.InlineKeyboardButton(self.locales[lang].view, callback_data = str(post_id) + ' for')]])
        message_content = types.InputTextMessageContent(self.locales[lang].private_message_for % scope_string)
        return types.InlineQueryResultArticle(
            id = '1', title = self.locales[lang].for_title % scope_string,
            input_message_content = message_content,
            reply_markup = keyboard,
            description = body,
            thumb_url = 'https://i.imgur.com/hHIkDSu.png')

    def mode_except(self, lang: str, post_id, body, scope_string):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard =
            [[types.InlineKeyboardButton(self.locales[lang].view, callback_data = str(post_id) + ' except')]])
        message_content = types.InputTextMessageContent(self.locales[lang].private_message_except % scope_string)
        return types.InlineQueryResultArticle(
            id = '2', title = self.locales[lang].except_title % scope_string,
            input_message_content = message_content,
            reply_markup = keyboard,
            description = body,
            thumb_url = 'https://i.imgur.com/S6OZMHd.png')

class Keyboards:
    def info_keyboard(self):
        return types.InlineKeyboardMarkup(inline_keyboard=
             [[types.InlineKeyboardButton('🇺🇸 English',    url='https://teletype.in/@undrcrxwn/hidethisbot_en'),
               types.InlineKeyboardButton('🇵🇱 Polski',     url='https://teletype.in/@undrcrxwn/hidethisbot_pl')],
              [types.InlineKeyboardButton('🇷🇺 Русский',    url='https://teletype.in/@undrcrxwn/hidethisbot_ru'),
               types.InlineKeyboardButton('🇺🇦 Українська', url='https://teletype.in/@undrcrxwn/hidethisbot_ua')],
              [types.InlineKeyboardButton('🇮🇹 Italiano',   url='https://teletype.in/@undrcrxwn/hidethisbot_it'),
               types.InlineKeyboardButton('🇨🇿 Čeština',    url='https://teletype.in/@undrcrxwn/hidethisbot_cz')]])

class Media:
    def group_greeting_sticker_id(self):
        return random.choice(('CAACAgIAAxkBAAECkihg7Y5tYnlKz9jRe6QCNOyvEZri2wACSQ4AAliyaUuDPYCgY_2GXiAE',
                              'CAACAgIAAxkBAAECkilg7Y5tzJPtIX4UMDgYaoxD6zcrogAC8Q0AAvMraEvkpXQDG5qEbyAE',
                              'CAACAgIAAxkBAAECkipg7Y5tQk6MZlccqoudX9PEnxPbUwACfBAAAhJpcEuU9SdfdRAPdiAE'))

class Resources:
    def __init__(self, locales: LocalesDict):
        self.query_results = QueryResults(locales)
        self.keyboards = Keyboards()
        self.media = Media()
