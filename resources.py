from aiogram import types

class Messages:
    def info(self):
        return ('If you still have questions after reading the article, '
                'you can leave them right here, contact support or simply '
                'ask for help in our public chat.\n\n'
                '👥 Public chat: @hidethisbot_chat\n'
                '⚙ Support: @undrcrxwn')

    def info_keyboard(self):
        return types.InlineKeyboardMarkup(inline_keyboard=
             [[types.InlineKeyboardButton('🇺🇸 English',    url='https://teletype.in/@undrcrxwn/hidethisbot_en'),
               types.InlineKeyboardButton('🇵🇱 Polski',     url='https://teletype.in/@undrcrxwn/hidethisbot_pl')],
              [types.InlineKeyboardButton('🇷🇺 Русский',    url='https://teletype.in/@undrcrxwn/hidethisbot_ru'),
               types.InlineKeyboardButton('🇺🇦 Українська', url='https://teletype.in/@undrcrxwn/hidethisbot_ua')],
              [types.InlineKeyboardButton('🇮🇹 Italiano',   url='https://teletype.in/@undrcrxwn/hidethisbot_it'),
               types.InlineKeyboardButton('🇨🇿 Čeština',    url='https://teletype.in/@undrcrxwn/hidethisbot_cz')]])

class QueryResults:
    def username_needed_to_use(self, bot_user):
        message_content = types.InputTextMessageContent(
           ('To use [' + bot_user.full_name + ']'
            '(t.me/' + bot_user.username + ') your account needs '
            'to have a username (e. g. @​my\_acc or @​durov).\n\n'
            'To set up your personal username visit *Settings ➩ Username*.'),
            disable_web_page_preview = True,
            parse_mode = 'markdown')
        return types.InlineQueryResultArticle(
            id = '1', title = 'Sorry, we cannot process your request',
            input_message_content = message_content,
            description = ('To use ' + bot_user.full_name + ' your account needs '
                           'to have a username (e. g. @my_acc or @durov).'),
            thumb_url = 'https://i.imgur.com/xblMvAx.png')

    def mode_for(self, post_id, body, scope_string):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard =
            [[types.InlineKeyboardButton("View", callback_data = str(post_id) + ' for')]])
        message_content = types.InputTextMessageContent(
            'Private message for ' + scope_string + '.',
            disable_web_page_preview = True)
        return types.InlineQueryResultArticle(
            id = '1', title = 'For ' + scope_string,
            input_message_content = message_content,
            reply_markup = keyboard,
            description = body,
            thumb_url = 'https://i.imgur.com/hHIkDSu.png')

    def mode_except(self, post_id, body, scope_string):
        keyboard = types.InlineKeyboardMarkup(inline_keyboard =
            [[types.InlineKeyboardButton("View", callback_data = str(post_id) + ' except')]])
        message_content = types.InputTextMessageContent(
            'Private message for everyone except ' + scope_string + '.',
            disable_web_page_preview = True)
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

    def username_needed_to_view(self):
        return ('To view hidden content your account needs to have a username'
                '(e. g. @my_acc or @durov).\n\n'
                'To set up your personal username visit Settings ➩ Username.')

class Resources:
    def __init__(self):
        self.messages = Messages()
        self.query_results = QueryResults()
        self.callback_responses = CallbackResponses()
