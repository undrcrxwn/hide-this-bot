import telebot
from telebot import types

class Messages:
    def info(self):
        return ('If you still have questions after reading the article, '
                'feel free to leave them here for the developer to answer them.')

    def info_keyboard(self):
        return types.InlineKeyboardMarkup([[types.InlineKeyboardButton('🇺🇸 English',    url='https://teletype.in/@undrcrxwn/hidethisbot_en')],
                                           [types.InlineKeyboardButton('🇷🇺 Русский',    url='https://teletype.in/@undrcrxwn/hidethisbot_ru'),
                                            types.InlineKeyboardButton('🇺🇦 Українська', url='https://teletype.in/@undrcrxwn/hidethisbot_ua')],
                                           [types.InlineKeyboardButton('🇵🇱 Polski',     url='https://teletype.in/@undrcrxwn/hidethisbot_pl'),
                                            types.InlineKeyboardButton('🇮🇹 Italiano',   url='https://teletype.in/@undrcrxwn/hidethisbot_it')]])

class QueryResults:
    def __init__(self, bot: telebot.TeleBot):
        self.bot = bot

    def username_needed_to_use(self):
        return types.InlineQueryResultArticle('1', 'Sorry, we cannot process your request',
               types.InputTextMessageContent(
                             ('To use [' + self.bot.get_me().full_name + ']'
                              '(t.me/' + self.bot.get_me().username + ') your account needs '
                              'to have a username (e. g. @​my\_acc or @​durov).\n\n'
                              'To set up your personal username visit *Settings ➩ Username*.'),
                              disable_web_page_preview=True,
                              parse_mode='markdown'),
               description = ('To use ' + self.bot.get_me().full_name + ' your account needs '
                              'to have a username (e. g. @my_acc or @durov).'),
               thumb_url   =  'https://i.imgur.com/xblMvAx.png')

    def mode_for(self, post_id, body, scope_string):
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("View", callback_data=str(post_id) + ' for')
        keyboard.add(button)
        return types.InlineQueryResultArticle('1', 'For ' + scope_string,
               types.InputTextMessageContent(
                             'Private message for ' + scope_string + '.',
                             disable_web_page_preview=True),
               keyboard,
               description = body,
               thumb_url   = 'https://i.imgur.com/hHIkDSu.png')

    def mode_except(self, post_id, body, scope_string):
        keyboard = types.InlineKeyboardMarkup()
        keyboard.add(types.InlineKeyboardButton("View", callback_data=str(post_id) + ' except'))
        return types.InlineQueryResultArticle('2', 'Except ' + scope_string,
               types.InputTextMessageContent(
                             'Private message for everyone except ' + scope_string + '.',
                             disable_web_page_preview=True),
               keyboard,
               description = body,
               thumb_url   = 'https://i.imgur.com/S6OZMHd.png')

class CallbackResponses:
    def not_allowed(self):
        return 'You are not allowed to view this content.'

    def not_accessible(self):
        return 'This content is no longer accessible.'

    def username_needed_to_view(self):
        return ('To view hidden content your account needs to have a username'
                '(e. g. @my_acc or @durov).\n\n'
                'To set up your personal username visit Settings ➩ Username.')

class Resources:
    def __init__(self, bot: telebot.TeleBot):
        self.messages = Messages()
        self.query_results = QueryResults(bot)
        self.callback_responses = CallbackResponses()
