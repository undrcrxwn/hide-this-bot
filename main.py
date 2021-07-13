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

def get_formatted_username_or_id(user: types.User):
    return 'id' + str(user.id) if user.username is None else '@' + user.username

def get_post(id: int):
    return execute_read_query('SELECT * FROM posts WHERE id = %s' % str(id))[0]

def insert_post(id: int, author: int, content: str, scope: set):
    execute_query('INSERT INTO posts (id, author, content, scope, creation_time) '
                  'VALUES (%s, %s, %s, %s, NOW());',
                  (id, author, content, ' '.join(scope).replace('@', '').lower()))

@dp.callback_query_handler()
async def callback_inline(call: types.inline_query):
    try:
        target = call.from_user
        (id, mode) = str(call.data).split(' ')
        try:
            post = get_post(id)
        except Exception as e:
            logger.error(e)
            logger.warning('#' + id + ' cannot be reached by ' + get_formatted_username_or_id(target))
            await bot.answer_callback_query(call.id, text = rsc.callback_responses.not_accessible(), show_alert = True)
            return

        (_, author, body, scope, creation_time) = post
        access_granted = False
        if not target.username:
            access_granted = mode == 'except' or target.id == author
        elif mode == 'for':
            access_granted = target.id == author or target.username.lower() in scope.split(' ')
        elif mode == 'except':
            access_granted = target.username.lower() not in scope.split(' ')

        if access_granted:
            logger.info('#' + id + ': ' + get_formatted_username_or_id(target) + ' - access granted')
            await bot.answer_callback_query(call.id, body
                .replace('{username}', get_formatted_username_or_id(target))
                .replace('{name}', target.full_name)
                .replace('{uid}', 'id' + str(target.id))
                .replace('{lang}', target.language_code)
                .replace('{pid}', '#' + id)
                .replace('{ts}', str(creation_time))
                .replace('{now}', str(datetime.now()))
                .replace('{date}', datetime.now().strftime('%Y-%m-%d'))
                .replace('{time}', datetime.now().strftime('%H:%M')),
                True)
        else:
            logger.info('#' + id + ': ' + get_formatted_username_or_id(target) + ' - access denied')
            await bot.answer_callback_query(call.id, rsc.callback_responses.not_allowed(), True)
    except Exception as e:
        logger.error(e)

@dp.inline_handler(lambda query: re.match(r'^.+( @\w+)+$', query.query.replace('\n', ' ')))
async def query_hide(inline_query: types.InlineQuery):
    try:
        target = inline_query.from_user
        r = re.compile(r'( @\w+)+$')
        body = r.sub('', inline_query.query)
        scope = inline_query.query[len(body) + 1:].split(' ')
        row_id = randint(0, 100000000)
        insert_post(row_id, target.id, body, scope)
        if get_post(row_id):
            logger.info('#' + str(row_id) + ' has been inserted by ' + get_formatted_username_or_id(target))
        else:
            logger.warning('#' + str(row_id) + ' cannot be inserted by ' + get_formatted_username_or_id(target))

        formatted_scope = ', '.join(scope[:-1])
        if len(scope) > 1:
            formatted_scope += ' and ' + scope[-1]
        else:
            formatted_scope = scope[0]

        await bot.answer_inline_query(inline_query.id,
           [rsc.query_results.mode_for(row_id, body, formatted_scope),
            rsc.query_results.mode_except(row_id, body, formatted_scope)],
            cache_time = 0)
    except Exception as e:
        logger.error(e)

@dp.inline_handler()
async def query_hide(inline_query: types.InlineQuery):
    await bot.answer_inline_query(inline_query.id, [],
                                  switch_pm_text = 'How to use this bot?',
                                  switch_pm_parameter = 'start')

@dp.message_handler(commands = ['start', 'help', 'info'])
async def send_info(message: types.Message):
    try:
        if message.chat.id in ignored_chat_ids: return
        Thread(target = ignore, args = (message.chat.id, 1)).start()
        await bot.send_message(message.chat.id,
                               text = rsc.messages.info(),
                               reply_markup = rsc.messages.info_keyboard(),
                               disable_web_page_preview = True)
    except Exception as e:
        logger.error(e)

@dp.my_chat_member_handler(lambda message: message.new_chat_member.status == 'member',
                           chat_type = (types.ChatType.GROUP, types.ChatType.SUPERGROUP))
async def send_group_greeting(message: types.ChatMemberUpdated):
    try:
        await bot.send_sticker(message.chat.id, rsc.messages.group_greeting_sticker_id())
        await bot.send_message(message.chat.id,
                               text = rsc.messages.group_greeting(await bot.get_me()),
                               parse_mode = 'html',
                               reply_markup = rsc.messages.group_greeting_keyboard(await bot.get_me()),
                               disable_web_page_preview = True)
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    try:
        execute_query("""
            CREATE TABLE IF NOT EXISTS posts (
                id INTEGER PRIMARY KEY,
                author INTEGER,
                content TEXT,
                scope TEXT,
                creation_time TIMESTAMP);
                """)

        logger.info('Start polling...')
        executor.start_polling(dp, skip_updates = True)
    except Exception as e:
        logger.error(e)
