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
    result = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        connection.commit()
        try:
            result = cursor.fetchall()
        except:
            pass
    except Exception as e:
        logger.error(e)
        connection.rollback()
        logger.info('transaction rollback: "' + query + '"')
    return result

def execute_read_query(query, data = None):
    result = None
    try:
        cursor = connection.cursor()
        cursor.execute(query, data)
        try:
            result = cursor.fetchall()
        except:
            pass
    except Exception as e:
        logger.error(e)
    return result

def get_formatted_username_or_id(user: types.User):
    return 'id' + str(user.id) if user.username is None else '@' + user.username

def get_post(post_id: int):
    result = None
    try:
        result = execute_read_query('SELECT * FROM posts WHERE id = %s', (str(post_id),))[0]
    except Exception as e:
        logger.error(e)

    if result is None:
        logger.warning('#' + str(post_id) + ' cannot be reached')
    return result

def insert_post(post_id: int, author: types.User, content: str, scope: list = None):
    result = None
    try:
        scope_string = '' if scope is None else ' '.join(scope).lower()
        result = execute_query('INSERT INTO posts (id, author, content, scope, creation_time) '
                               'VALUES (%s, %s, %s, %s, NOW()) RETURNING id',
                               (post_id, author.id, content, scope_string))
    except Exception as e:
        logger.error(e)

    if result is None:
        logger.warning('#' + str(post_id) + ' cannot be inserted by ' + get_formatted_username_or_id(author))
    else:
        logger.info('#' + str(post_id) + ' has been inserted by ' + get_formatted_username_or_id(author))
    return result

def update_user_in_scope(post_id: int, username: str, user_id: int):
    try:
        (_, author, body, scope_string, creation_time) = get_post(post_id)
        scope = scope_string.split(' ')
        for i, mention in enumerate(scope):
            if mention == username:
                scope[i] = str(user_id)
        execute_query('UPDATE posts '
                      'SET scope = %s '
                      'WHERE id = %s;',
                      (' '.join(scope), post_id))
    except Exception as e:
        logger.error(e)
        logger.warning('cannot update @' +  username + ' to id: ' + str(user_id) + ' in scope #' + str(post_id))

@dp.inline_handler(lambda query: re.match(inline_query_regex, query.query.replace('\n', ' ')))
async def inline_query_hide(inline_query: types.InlineQuery):
    try:
        target = inline_query.from_user
        body = scope_regex.sub('', inline_query.query)
        if len(body) > 200:
            await inline_query.answer([rsc.query_results.message_too_long(target.language_code)])
            return

        raw_scope = re.sub(r'(id)([0-9]+)', r'\g<2>', inline_query.query[len(body) + 1:]).split(' ')
        marker = set()
        scope = [not marker.add(x.casefold()) and x for x in raw_scope if x.casefold() not in marker]
        post_id = random.randint(0, 100000000)
        insert_post(post_id, target, body, scope)

        formatted_scope = ', '.join(scope[:-1])
        if len(scope) > 1:
            formatted_scope += ' %s ' % locales[target.language_code].and_connector + scope[-1]
        else:
            formatted_scope = scope[0]

        await inline_query.answer([rsc.query_results.mode_for(target.language_code, post_id, body, formatted_scope),
                                   rsc.query_results.mode_except(target.language_code, post_id, body, formatted_scope)],
                                   cache_time = 0)
    except Exception as e:
        logger.error(e)
        logger.warning('cannot handle inline query hide from ' +
                       get_formatted_username_or_id(inline_query.from_user) + ' '
                       'with payload: "' + inline_query.query + '"')

@dp.inline_handler(lambda query: len(query.query) > 0)
async def inline_query_spoiler(inline_query: types.InlineQuery):
    try:
        target = inline_query.from_user
        body = inline_query.query
        if len(body) > 200:
            await inline_query.answer([rsc.query_results.message_too_long(target.language_code)])
            return

        post_id = random.randint(0, 100000000)
        insert_post(post_id, target, body)
        await inline_query.answer([rsc.query_results.spoiler(target.language_code, post_id, body)])
    except Exception as e:
        logger.error(e)
        logger.warning('cannot handle inline query spoiler from ' +
                       get_formatted_username_or_id(inline_query.from_user) + ' '
                       'with payload: "' + inline_query.query + '"')

@dp.inline_handler()
async def inline_query_help(inline_query: types.InlineQuery):
    try:
        await inline_query.answer([], switch_pm_text = locales[inline_query.from_user.language_code].how_to_use,
                                  switch_pm_parameter  = 'how_to_use')
    except Exception as e:
        logger.error(e)
        logger.warning('cannot handle inline query help from ' +
                       get_formatted_username_or_id(inline_query.from_user) + ' '
                       'with payload: "' + inline_query.query + '"')

@dp.callback_query_handler()
async def callback_query(call: types.CallbackQuery):
    try:
        target = call.from_user
        (post_id, mode) = str(call.data).split(' ')
        try:
            post = get_post(post_id)
        except Exception as e:
            logger.error(e)
            logger.warning('#' + post_id + ' cannot be reached by ' + get_formatted_username_or_id(target))
            await bot.answer_callback_query(call.id, text = locales[target.language_code].not_accessible, show_alert = True)
            return

        (_, author, body, scope_string, creation_time) = post
        scope = scope_string.split(' ')
        access_granted = False
        if mode == 'spoiler':
            access_granted = True
        elif mode == 'for':
            if target.username and target.username.lower() in scope:
                access_granted = True
                update_user_in_scope(post_id, target.username.lower(), target.id)
            else:
                access_granted = target.id == author or str(target.id) in scope
        elif mode == 'except':
            if target.username and target.username.lower() in scope:
                update_user_in_scope(post_id, target.username.lower(), target.id)
            else:
                access_granted = str(target.id) not in scope

        if access_granted:
            logger.info('#' + post_id + ': ' + get_formatted_username_or_id(target) + ' - access granted')
            await bot.answer_callback_query(call.id, body
                .replace('{username}', get_formatted_username_or_id(target))
                .replace('{name}', target.full_name)
                .replace('{uid}', 'id' + str(target.id))
                .replace('{lang}', 'unknown' if target.language_code is None else target.language_code)
                .replace('{pid}', '#' + post_id)
                .replace('{ts}', str(creation_time))
                .replace('{now}', str(datetime.now()))
                .replace('{date}', datetime.now().strftime('%Y-%m-%d'))
                .replace('{time}', datetime.now().strftime('%H:%M')),
                True)
        else:
            logger.info('#' + post_id + ': ' + get_formatted_username_or_id(target) + ' - access denied')
            await call.answer(locales[target.language_code].not_allowed, True)
    except Exception as e:
        logger.error(e)
        logger.warning('cannot handle callback query from ' +
                       get_formatted_username_or_id(call.from_user) + ' '
                       'with payload: "' + call.data + '"')

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
        logger.warning('cannot send info to chat_id: ' + message.chat.id)

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
