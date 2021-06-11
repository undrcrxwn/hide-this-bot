import asyncio
import os
import time
import re
from threading import Thread
from loguru import logger
import psycopg2
from psycopg2 import OperationalError
import telebot
from telebot import types
from random import *

bot = telebot.TeleBot(os.environ.get('API_TOKEN'))
connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
logger.add(os.environ.get('LOG_PATH'), level='DEBUG')
ignored_chat_ids = set()

def ignore(chat_id, timeout):
    ignored_chat_ids.add(chat_id)
    time.sleep(timeout)
    ignored_chat_ids.remove(chat_id)

def execute_query(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        connection.commit()
    except OperationalError as e:
        logger.error(f'The error "{e}" occurred')
    except Exception as e:
        logger.error(e)

def execute_read_query(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except OperationalError as e:
        logger.error(f'The error "{e}" occurred')
    except Exception as e:
        logger.error(e)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        target = call.from_user.username
        if not target:
            bot.answer_callback_query(call.id,
                                      text='To view hidden content your account needs to have a username ' +
                                           '(e. g. @my_acc or @durov).\n\n' +
                                           'To set up your personal username go to Settings ➩ Username.',
                                      show_alert=True)
            return

        (id, mode) = str(call.data).split(' ')
        try:
            post = execute_read_query('SELECT * FROM posts WHERE id = ' + id)[0]
        except Exception as e:
            logger.error(e)
            logger.info('#' + id + ' cannot be reached by @' + call.from_user.username)
            bot.answer_callback_query(call.id, text='This content is no longer accessible.', show_alert=True)
            return
        (_, author, body, scope) = post

        access_granted = False
        if mode == 'for':
            access_granted = target.lower() == author or target.lower() in scope.split(' ')
        elif mode == 'except':
            access_granted = target.lower() not in scope.split(' ')

        if access_granted:
            logger.info('#' + id + ': @' + call.from_user.username + ' - access granted')
            bot.answer_callback_query(call.id, text=body, show_alert=True)
        else:
            logger.info('#' + id + ': @' + call.from_user.username + ' - access denied')
            bot.answer_callback_query(call.id, text='You are not allowed to view this content.', show_alert=True)
    except Exception as e:
        logger.error(e)

@bot.inline_handler(lambda query: re.match(r'^.+ (@.+)$', query.query))
def query_hide(inline_query):
    try:
        target = inline_query.from_user.username
        if not target:
            r = types.InlineQueryResultArticle('1', 'Sorry, we cannot process your request',
                                               types.InputTextMessageContent('To use [' + bot.get_me().full_name + ']' +
                                                           '(t.me/' + bot.get_me().username + ') your account needs ' +
                                                           'to have a username (e. g. @​my\_acc or @​durov).\n\n' +
                                                           'To set up your personal username visit *Settings ➩ Username*.',
                                                           disable_web_page_preview=True,
                                                           parse_mode='markdown'),
                                               description='To use ' + bot.get_me().full_name + ' your account needs ' +
                                                           'to have a username (e. g. @my_acc or @durov).',
                                               thumb_url='https://i.imgur.com/xblMvAx.png')
            bot.answer_inline_query(inline_query.id, [r])
            return

        r = re.compile(r'( @.+)+$')
        body = r.sub('', inline_query.query)
        scope = list(dict.fromkeys(inline_query.query[len(body) + 1:].split(' ')))
        if '' in scope:
            scope.remove('')

        row_id = str(randint(0, 100000000))
        execute_query("""
        INSERT INTO posts (id, author, content, scope)
        VALUES (""" + row_id + ", '" + target.lower() + "', '" +
                body + "', '" + ' '.join(scope).lower().replace('@', '') + "');")
        logger.info('#' + row_id + ' has been created by @' + target)

        formatted_scope = ', '.join(scope[:-1])
        if len(scope) > 1:
            formatted_scope += ' and ' + scope[-1]
        else:
            formatted_scope = scope[0]

        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("View", callback_data=row_id + ' for')
        keyboard.add(button)
        r1 = types.InlineQueryResultArticle('1', 'For ' + formatted_scope,
                                            types.InputTextMessageContent('Private message for ' + formatted_scope + '.',
                                                                          disable_web_page_preview=True),
                                            keyboard,
                                            description=body,
                                            thumb_url='https://i.imgur.com/hHIkDSu.png')
        keyboard = types.InlineKeyboardMarkup()
        button = types.InlineKeyboardButton("View", callback_data=row_id + ' except')
        keyboard.add(button)
        r2 = types.InlineQueryResultArticle('2', 'Except ' + formatted_scope,
                                            types.InputTextMessageContent('Private message for everyone except ' + formatted_scope + '.',
                                                                          disable_web_page_preview=True),
                                            keyboard,
                                            description=body,
                                            thumb_url='https://i.imgur.com/S6OZMHd.png')
        bot.answer_inline_query(inline_query.id, [r1, r2])
    except Exception as e:
        logger.error(e)

@bot.message_handler()
def send_info(message):
    try:
        if message.chat.id in ignored_chat_ids: return
        Thread(target=ignore, args=(message.chat.id, 5)).start()

        bot.send_message(message.chat.id,
                         '[🇺🇸 teletype/instructions](https://teletype.in/@undrcrxwn/hidethisbot_en)',
                         parse_mode='markdown')
        bot.send_message(message.chat.id,
                         '[🇷🇺 teletype/instructions](https://teletype.in/@undrcrxwn/hidethisbot_ru)',
                         parse_mode='markdown')
    except Exception as e:
        logger.error(e)

def main_loop():
    bot.polling(True)
    while True:
        time.sleep(3)

if __name__ == '__main__':
    try:
        execute_query("""
            CREATE TABLE IF NOT EXISTS posts (
              id INTEGER PRIMARY KEY,
              author TEXT,
              content TEXT,
              scope TEXT);
              """)

        logger.info('Starting main_loop...')
        main_loop()
    except Exception as e:
        logger.error(e)
