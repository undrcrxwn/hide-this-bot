import os
import random
import re
import time
from datetime import datetime
from threading import Thread

import psycopg2
from aiogram import Bot, Dispatcher, executor, types
from loguru import logger

from locales import locales
from resources import Resources

logger.add(os.environ['LOG_PATH'], level = 'DEBUG')
rsc = Resources(locales)

inline_query_regex = re.compile(r'^.+([ \n](@\w+|id[0-9]+))+$')
scope_regex = re.compile(r'([ \n](@\w+|id[0-9]+))+$')

ignored_chat_ids = set()
connection = psycopg2.connect(os.environ['DATABASE_URL'], sslmode = 'require')
bot = Bot(token = os.environ['API_TOKEN'])
dp = Dispatcher(bot)

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

def execute_read_query(query, data = None):
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        result = cursor.fetchall()
        return result
    except Exception as e:
        logger.error(e)

def get_formatted_username_or_id(user: types.User):
    return 'id' + str(user.id) if user.username is None else '@' + user.username

def get_post(pid: int):
    return execute_read_query('SELECT * FROM posts WHERE id = %s', (str(pid),))[0]

def insert_post(pid: int, author: int, content: str, scope: list):
    execute_query('INSERT INTO posts (id, author, content, scope, creation_time) '
                  'VALUES (%s, %s, %s, %s, NOW());',
                  (pid, author, content, ' '.join(scope).replace('@', '').lower()))

def update_user_in_scope(pid: int, username: str, user_id: int):
    (_, author, body, scope, creation_time) = get_post(pid)
    execute_query('UPDATE posts '
                  'SET scope = %s '
                  'WHERE id = %s;',
                  (scope.replace(username, str(user_id)), pid))

@dp.callback_query_handler()
async def callback_inline(call: types.CallbackQuery):
    try:
        target = call.from_user
        (pid, mode) = str(call.data).split(' ')
        try:
            post = get_post(pid)
        except Exception as e:
            logger.error(e)
            logger.warning('#' + pid + ' cannot be reached by ' + get_formatted_username_or_id(target))
            await bot.answer_callback_query(call.id, text = locales[target.language_code].not_accessible, show_alert = True)
            return

        (_, author, body, scope, creation_time) = post
        access_granted = False
        if target.username is None:
            access_granted = mode == 'except' or target.id == author
        elif mode == 'for':
            if target.username.lower() in scope.split(' '):
                access_granted = True
                update_user_in_scope(pid, target.username.lower(), target.id)
            else:
                access_granted = target.id == author or str(target.id) in scope.split(' ')
        elif mode == 'except':
            if target.username.lower() in scope.split(' '):
                access_granted = False
                update_user_in_scope(pid, target.username.lower(), target.id)
            else:
                access_granted = target.id == author and str(target.id) not in scope.split(' ')

        if access_granted:
            logger.info('#' + pid + ': ' + get_formatted_username_or_id(target) + ' - access granted')
            await bot.answer_callback_query(call.id, body
                .replace('{username}', get_formatted_username_or_id(target))
                .replace('{name}', target.full_name)
                .replace('{uid}', 'id' + str(target.id))
                .replace('{lang}', target.language_code)
                .replace('{pid}', '#' + pid)
                .replace('{ts}', str(creation_time))
                .replace('{now}', str(datetime.now()))
                .replace('{date}', datetime.now().strftime('%Y-%m-%d'))
                .replace('{time}', datetime.now().strftime('%H:%M')),
                True)
        else:
            logger.info('#' + pid + ': ' + get_formatted_username_or_id(target) + ' - access denied')
            await call.answer(locales[target.language_code].not_allowed, True)
    except Exception as e:
        logger.error(e)

@dp.inline_handler(lambda query: re.match(inline_query_regex, query.query.replace('\n', ' ')))
async def query_hide(inline_query: types.InlineQuery):
    try:
        target = inline_query.from_user
        body = scope_regex.sub('', inline_query.query)
        if len(body) > 200:
            await inline_query.answer([rsc.query_results.message_too_long(target.language_code)])
            return

        raw_scope = re.sub(r'(id)([0-9]+)', r'\g<2>', inline_query.query[len(body) + 1:]).split(' ')
        marker = set()
        scope = [not marker.add(x.casefold()) and x for x in raw_scope if x.casefold() not in marker]
        pid = random.randint(0, 100000000)
        insert_post(pid, target.id, body, scope)
        if get_post(pid):
            logger.info('#' + str(pid) + ' has been inserted by ' + get_formatted_username_or_id(target))
        else:
            logger.warning('#' + str(pid) + ' cannot be inserted by ' + get_formatted_username_or_id(target))

        formatted_scope = ', '.join(scope[:-1])
        if len(scope) > 1:
            formatted_scope += ' %s ' % locales[target.language_code].and_connector + scope[-1]
        else:
            formatted_scope = scope[0]

        await inline_query.answer([rsc.query_results.mode_for(target.language_code, pid, body, formatted_scope),
                                   rsc.query_results.mode_except(target.language_code, pid, body, formatted_scope)],
                                   cache_time = 0)
    except Exception as e:
        logger.error(e)

@dp.inline_handler()
async def query_hide(inline_query: types.InlineQuery):
    await inline_query.answer([], switch_pm_text = locales[inline_query.from_user.language_code].how_to_use,
                                  switch_pm_parameter = 'how_to_use')

@dp.message_handler(commands = ['start', 'help', 'info'])
async def send_info(message: types.Message):
    try:
        if message.chat.id in ignored_chat_ids:
            return
        Thread(target = ignore, args = (message.chat.id, 1)).start()
        await message.answer(text = locales[message.from_user.language_code].info_message,
                             reply_markup = rsc.keyboards.info_keyboard(),
                             disable_web_page_preview = True)
    except Exception as e:
        logger.error(e)

@dp.my_chat_member_handler(lambda message: message.new_chat_member.status == 'member',
                           chat_type = (types.ChatType.GROUP, types.ChatType.SUPERGROUP))
async def send_group_greeting(message: types.ChatMemberUpdated):
    try:
        bot_user = await bot.get_me()
        await bot.send_sticker(message.chat.id, rsc.media.group_greeting_sticker_id())
        await bot.send_message(message.chat.id,
                               text = locales[message.from_user.language_code].group_greeting_message
                                    % (bot_user.full_name, bot_user.username),
                               parse_mode = 'html',
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
