from aiogram import types
import random

class Messages:
    def group_greeting(self, bot_user: types.User):
        return ('👋 Hi! My name is ' + bot_user.full_name + ' and I can help you send private messages '
                'that only certain people can view. To learn more send /start@' + bot_user.username + ' '
                'and feel free to ask for help in our <a href="t.me/hidethisbot_chat">public community</a> '
                'if you\'ve got any questions.\n\n'
                '🤝 To talk to me right here do the following: '
                '<b>Group — Edit — Administrators — Add Admin — ' + bot_user.full_name + '</b>. This will '
                'let me see your messages and send replies')

    def info(self):
        return ('If you still have questions after reading the article, '
                'you can leave them right here, contact support or simply '
                'ask for help in our public chat.\n\n'
                '👥 Public chat: @hidethisbot_chat\n'
                '⚙ Support: @undrcrxwn')

class QueryResults:
    def message_too_long(self):
        message_content = types.InputTextMessageContent(
            '🥺 Sorry, your message can\'t be sent as it exceeds the limit of 200 characters.')
        return types.InlineQueryResultArticle(
            id = '1', title = 'Your message is too long',
            input_message_content = message_content,
            description = ('Please shorten the length of your message so that '
                           'it doesn\'t exceed the limit of 200 characters.'),
            thumb_url = 'https://i.imgur.com/xblMvAx.png')

    def mode_for(self, post_id, body, scope_string):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard =
            [[types.InlineKeyboardButton('View', callback_data = str(post_id) + ' for')]])
        message_content = types.InputTextMessageContent(
            'Private message for ' + scope_string + '.')
        return types.InlineQueryResultArticle(
            id = '1', title = 'For ' + scope_string,
            input_message_content = message_content,
            reply_markup = keyboard,
            description = body,
            thumb_url = 'https://i.imgur.com/hHIkDSu.png')

    def mode_except(self, post_id, body, scope_string):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard =
            [[types.InlineKeyboardButton('View', callback_data = str(post_id) + ' except')]])
        message_content = types.InputTextMessageContent(
            'Private message for everyone except ' + scope_string + '.')
        return types.InlineQueryResultArticle(
            id = '2', title = 'Except ' + scope_string,
            input_message_content = message_content,
            reply_markup = keyboard,
            description = body,
            thumb_url = 'https://i.imgur.com/S6OZMHd.png')

class CallbackResponses:
    def not_allowed(self):
        return 'You are not allowed to view this content.'

    def not_accessible(self):
        return 'This content is no longer accessible.'

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
    def __init__(self):
        self.messages = Messages()
        self.query_results = QueryResults()
        self.callback_responses = CallbackResponses()
        self.keyboards = Keyboards()
        self.media = Media()
