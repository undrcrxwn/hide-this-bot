import os
import time
from datetime import datetime
import re
from threading import Thread
from loguru import logger
import psycopg2
from random import *
from resources import *
from aiogram import Bot, Dispatcher, executor, types

connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode = 'require')
bot = Bot(token = os.environ['API_TOKEN'])
dp = Dispatcher(bot)
rsc = Resources()
logger.add(os.environ['LOG_PATH'], level = 'DEBUG')
ignored_chat_ids = set()

def ignore(chat_id, timeout):
    ignored_chat_ids.add(chat_id)
    time.sleep(timeout)
    ignored_chat_ids.remove(chat_id)

def execute_query(query, data = None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
    except Exception as e:
        logger.error(e)
        connection.rollback()
        logger.info('transaction rollback: "' + query + '"')

def execute_read_query(query):
    try:
        cursor = connection.cursor()
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Exception as e:
        logger.error(e)

def get_post(id: int):
    return execute_read_query('SELECT * FROM posts WHERE id = %s' % str(id))[0]

def insert_post(id: int, author: str, content: str, scope: []):
    execute_query('INSERT INTO posts (id, author, content, scope) '
                  'VALUES (%s, %s, %s, %s);',
                  (id, author.lower(), content, ' '.join(scope).lower().replace('@', ''),))

@dp.callback_query_handler()
async def callback_inline(call):
    try:
        target = call.from_user.username
        if not target:
            await bot.answer_callback_query(call.id, rsc.callback_responses.username_needed_to_view(), True)
            return

        (id, mode) = str(call.data).split(' ')
        try:
            post = get_post(id)
        except Exception as e:
            logger.error(e)
            logger.warning('#' + id + ' cannot be reached by @' + call.from_user.username)
            await bot.answer_callback_query(call.id, text = rsc.callback_responses.not_accessible(), show_alert = True)
            return

        (_, author, body, scope) = post
        access_granted = False
        if mode == 'for':
            access_granted = target.lower() == author or target.lower() in scope.split(' ')
        elif mode == 'except':
            access_granted = target.lower() not in scope.split(' ')

        if access_granted:
            logger.info('#' + id + ': @' + call.from_user.username + ' - access granted')
            await bot.answer_callback_query(call.id, body
                                            .replace('{username}', '@' + call.from_user.username)
                                            .replace('{name}', call.from_user.full_name)
                                            .replace('{uid}', 'id' + str(call.from_user.id))
                                            .replace('{pid}', '#' + id)
                                            .replace('{time}', str(datetime.now())),
                                            True)
        else:
            logger.info('#' + id + ': @' + call.from_user.username + ' - access denied')
            await bot.answer_callback_query(call.id, rsc.callback_responses.not_allowed(), True)
    except Exception as e:
        logger.error(e)

@dp.inline_handler(lambda query: re.match(r'^.+( @\w+)+$', query.query.replace('\n', ' ')))
async def query_hide(inline_query: types.InlineQuery):
    try:
        target = inline_query.from_user.username
        if not target:
            await bot.answer_inline_query(inline_query.id, [rsc.query_results.username_needed_to_use(await bot.get_me())])
            return

        r = re.compile(r'( @\w+)+$')
        body = r.sub('', inline_query.query)
        scope = list(dict.fromkeys(inline_query.query[len(body) + 1:].split(' ')))
        if '' in scope:
            scope.remove('')

        row_id = randint(0, 100000000)
        insert_post(row_id, target, body, scope)
        if get_post(row_id):
            logger.info('#' + str(row_id) + ' has been inserted by @' + target)
        else:
            logger.warning('#' + str(row_id) + ' cannot be inserted by @' + target)

        formatted_scope = ', '.join(scope[:-1])
        if len(scope) > 1:
            formatted_scope += ' and ' + scope[-1]
        else:
            formatted_scope = scope[0]

        await bot.answer_inline_query(inline_query.id,
           [rsc.query_results.mode_for(row_id, body, formatted_scope),
            rsc.query_results.mode_except(row_id, body, formatted_scope)])
    except Exception as e:
        logger.error(e)

@dp.inline_handler()
async def query_hide(inline_query: types.InlineQuery):
    await bot.answer_inline_query(inline_query.id, [],
                                  switch_pm_text = 'How to use this bot?',
                                  switch_pm_parameter = 'start')

@dp.message_handler(commands = ['start', 'help', 'info'])
async def send_info(message):
    try:
        if message.chat.id in ignored_chat_ids: return
        Thread(target = ignore, args = (message.chat.id, 1)).start()
        await bot.send_message(message.chat.id,
                               text = rsc.messages.info(),
                               reply_markup = rsc.messages.info_keyboard(),
                               disable_web_page_preview = True)
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    try:
        execute_query("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                author TEXT,
                content TEXT,
                scope TEXT);
                """)

        logger.info('Start polling...')
        executor.start_polling(dp, skip_updates = True)
    except Exception as e:
        logger.error(e)
