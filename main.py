import os
import random
import re
import time
from datetime import datetime
from threading import Thread

from aiogram import Bot, Dispatcher, executor, types
from loguru import logger

from locales import locales
from models import User, Post, PostMode
from resources import Resources
from utils import get_formatted_username_or_id

logger.add(os.environ['LOG_PATH'])
rsc = Resources(locales)

inline_query_regex = re.compile(r'^.+([ \n](@\w+|id[0-9]+))+$')
scope_regex = re.compile(r'([ \n](@\w+|id[0-9]+))+$')

ignored_chat_ids = set()
bot = Bot(token = os.environ['API_TOKEN'])
dp = Dispatcher(bot)

def ignore(chat_id, timeout):
    ignored_chat_ids.add(chat_id)
    time.sleep(timeout)
    ignored_chat_ids.remove(chat_id)

def create_post(author: User, content: str, scope: set = ()):
    try:
        result = Post.create(
            author = author,
            content = content,
            scope = ' '.join(scope).replace('@', ''),
            creation_time = datetime.now())
        logger.info('#' + str(result.get_id()) + ' has been created by ' + get_formatted_username_or_id(author))
        return result
    except Exception as e:
        logger.error('new post cannot be created by ' + get_formatted_username_or_id(author))
        logger.error(e)
        return

@dp.inline_handler(lambda query: re.match(inline_query_regex, query.query.replace('\n', ' ')))
async def inline_query_hide(inline_query: types.InlineQuery):
    try:
        target = User.get_or_create(inline_query.from_user)
        target.inline_queries_count += 1
        target.save()

        body = scope_regex.sub('', inline_query.query)
        if len(body) > 200:
            await inline_query.answer([rsc.query_results.message_too_long(target.language_code)])
            return

        raw_scope = re.sub(r'(id)([0-9]+)', r'\g<2>', inline_query.query[len(body) + 1:]).split(' ')
        marker = set()
        scope = [not marker.add(x.casefold()) and x for x in raw_scope if x.casefold() not in marker]
        post = create_post(target, body, set(scope))

        formatted_scope = ', '.join(scope[:-1])
        if len(scope) > 1:
            formatted_scope += ' %s ' % locales[target.language_code].and_connector + scope[-1]
        else:
            formatted_scope = scope[0]

        await inline_query.answer(
            [rsc.query_results.mode_for(target.language_code, post.get_id(), body, formatted_scope),
             rsc.query_results.mode_except(target.language_code, post.get_id(), body, formatted_scope)],
            cache_time = 0)
    except Exception as e:
        logger.error(e)
        logger.warning(
            'cannot handle inline query hide from ' +
            get_formatted_username_or_id(inline_query.from_user) +
            ' with payload: "' + inline_query.query + '"')

@dp.inline_handler(lambda query: len(query.query) > 0)
async def inline_query_spoiler(inline_query: types.InlineQuery):
    try:
        target = User.get_or_create(inline_query.from_user)
        target.inline_queries_count += 1
        target.save()

        body = inline_query.query
        if len(body) > 200:
            await inline_query.answer([rsc.query_results.message_too_long(target.language_code)])
            return

        post = create_post(target, body)
        await inline_query.answer([rsc.query_results.mode_spoiler(target.language_code, post.get_id(), body)])
    except Exception as e:
        logger.error(e)
        logger.warning(
            'cannot handle inline query spoiler from ' +
            get_formatted_username_or_id(inline_query.from_user) +
            ' with payload: "' + inline_query.query + '"')

@dp.inline_handler()
async def inline_query_help(inline_query: types.InlineQuery):
    try:
        await inline_query.answer(
            [], switch_pm_text = locales[inline_query.from_user.language_code].how_to_use,
            cache_time = 0,
            switch_pm_parameter  = 'how_to_use')
        target = User.get_or_create(inline_query.from_user)
        target.inline_queries_count += 1
        target.save()
    except Exception as e:
        logger.error(e)
        logger.warning(
            'cannot handle inline query help from ' +
            get_formatted_username_or_id(inline_query.from_user) +
            ' with payload: "' + inline_query.query + '"')

@dp.callback_query_handler()
async def callback_query(call: types.CallbackQuery):
    try:
        (post_id, mode) = str(call.data).split(' ')
        try:
            post = Post.get_by_id(post_id)
        except Exception as e:
            await call.answer(
                text = locales[call.from_user.language_code].not_accessible,
                show_alert = True)
            return

        target = User.get_or_create(call.from_user)
        if post.can_be_accessed_by(call.from_user, PostMode[mode]):
            logger.info('#' + post_id + ': ' + get_formatted_username_or_id(call.from_user) + ' - access granted')
            await call.answer(post.content
                .replace('{username}', get_formatted_username_or_id(call.from_user))
                .replace('{uid}', 'id' + str(target.user_id))
                .replace('{lang}', 'unknown' if target.language_code is None else target.language_code)
                .replace('{pid}', '#' + post_id)
                .replace('{created}', str(post.creation_time))
                .replace('{queries}', str(target.inline_queries_count))
                .replace('{first_interaction}', str(target.first_interaction_time))
                .replace('{dialog}', 'Yes' if target.has_dialog else 'No')
                .replace('{utc}', str(datetime.utcnow()))
                .replace('{date}', datetime.utcnow().strftime('%Y-%m-%d'))
                .replace('{time}', datetime.utcnow().strftime('%H:%M'))
                .replace('{name}', call.from_user.full_name)
                .replace('{first_name}', target.first_name)
                .replace('{last_name}', '' if target.last_name is None else target.last_name),
                True)
        else:
            logger.info('#' + post_id + ': ' + get_formatted_username_or_id(call.from_user) + ' - access denied')
            await call.answer(locales[call.from_user.language_code].not_allowed, True)
    except Exception as e:
        logger.error(e)
        logger.warning(
            'cannot handle callback query from ' +
            get_formatted_username_or_id(call.from_user) +
            ' with payload: "' + call.data + '"')

@dp.message_handler()
async def send_info(message: types.Message):
    try:
        if message.chat.id in ignored_chat_ids:
            return
        Thread(target = ignore, args = (message.chat.id, 1)).start()
        is_tracked_user = message.chat.type == types.ChatType.PRIVATE

        command = message.get_command()
        if (command is not None and
            command.lower().endswith((await bot.get_me()).username.lower())):
            command = command.split('@')[0]
        if command in ['/start', '/help', '/info']:
            is_tracked_user = True
            await message.answer(
                text = locales[message.from_user.language_code].info_message,
                reply_markup = rsc.keyboards.info_keyboard(),
                disable_web_page_preview = True)
        if is_tracked_user:
            target = User.get_or_create(message.from_user)
            target.has_dialog = True
            target.save()
    except Exception as e:
        logger.error(e)
        logger.warning('cannot send info to chat_id=' + str(message.chat.id))

@dp.my_chat_member_handler(
    lambda message: message.new_chat_member.status == types.ChatMemberStatus.MEMBER,
    chat_type = (types.ChatType.GROUP, types.ChatType.SUPERGROUP))
async def send_group_greeting(message: types.ChatMemberUpdated):
    try:
        bot_user = await bot.get_me()
        await bot.send_sticker(message.chat.id, rsc.media.group_greeting_sticker_id())
        await bot.send_message(
            message.chat.id,
            text = locales[message.from_user.language_code].group_greeting_message
                   % (bot_user.full_name, bot_user.username),
            parse_mode = 'html',
            disable_web_page_preview = True)
    except Exception as e:
        logger.error(e)

if __name__ == '__main__':
    try:
        logger.info('Start polling...')
        executor.start_polling(dp, skip_updates = True)
    except Exception as e:
        logger.error(e)
