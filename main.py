import os
import time
import re
from threading import Thread
from loguru import logger
import psycopg2
from psycopg2 import OperationalError
from random import *
from resources import *

bot = telebot.TeleBot(os.environ.get('API_TOKEN'))
connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode='require')
rsc = Resources(bot)
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
            bot.answer_callback_query(call.id, rsc.callback_responses.username_needed_to_view(), True)
            return

        (id, mode) = str(call.data).split(' ')
        try:
            post = execute_read_query('SELECT * FROM posts WHERE id = ' + id)[0]
        except Exception as e:
            logger.error(e)
            logger.info('#' + id + ' cannot be reached by @' + call.from_user.username)
            bot.answer_callback_query(call.id, text=rsc.callback_responses.not_accessible(), show_alert=True)
            return

        (_, author, body, scope) = post
        access_granted = False
        if mode == 'for':
            access_granted = target.lower() == author or target.lower() in scope.split(' ')
        elif mode == 'except':
            access_granted = target.lower() not in scope.split(' ')

        if access_granted:
            logger.info('#' + id + ': @' + call.from_user.username + ' - access granted')
            bot.answer_callback_query(call.id, body, True)
        else:
            logger.info('#' + id + ': @' + call.from_user.username + ' - access denied')
            bot.answer_callback_query(call.id, rsc.callback_responses.not_allowed(), True)
    except Exception as e:
        logger.error(e)

@bot.inline_handler(lambda query: re.match(r'^.+( @\w+)+$', query.query))
def query_hide(inline_query):
    try:
        target = inline_query.from_user.username
        if not target:
            bot.answer_inline_query(inline_query.id, [rsc.query_results.username_needed_to_use()])
            return

        r = re.compile(r'( @\w+)+$')
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

        bot.answer_inline_query(inline_query.id, [rsc.query_results.mode_for(row_id, body, formatted_scope),
                                                  rsc.query_results.mode_except(row_id, body, formatted_scope)])
    except Exception as e:
        logger.error(e)

@bot.message_handler()
def send_info(message):
    try:
        if message.chat.id in ignored_chat_ids: return
        Thread(target=ignore, args=(message.chat.id, 5)).start()

        bot.send_message(message.chat.id, rsc.messages.info_en(), parse_mode='markdown')
        bot.send_message(message.chat.id, rsc.messages.info_ru(), parse_mode='markdown')
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
