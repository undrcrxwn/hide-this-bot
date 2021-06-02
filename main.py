import os
import time
import re
from loguru import logger
import sqlite3
from sqlite3 import Error
import telebot
from telebot import types

bot = telebot.TeleBot(os.environ.get('API_TOKEN'))
connection = sqlite3.connect(os.environ.get('DB_PATH'), check_same_thread=False)
cursor = connection.cursor()
logger.add(os.environ.get('LOG_PATH'), level='DEBUG')

def execute_query(query):
    try:
        cursor.execute(query)
        connection.commit()
    except Error as e:
        logger.error(e)

def execute_read_query(query):
    try:
        cursor.execute(query)
        result = cursor.fetchall()
        return result
    except Error as e:
        logger.error(e)

@bot.callback_query_handler(func=lambda call: True)
def callback_inline(call):
    try:
        (id, mode) = str(call.data).split(' ')
        try:
            post = execute_read_query('SELECT * FROM posts WHERE id = ' + id)[0]
        except Exception as e:
            logger.error(e)
            logger.info('#' + id + ' cannot be reached')
            bot.answer_callback_query(call.id, text='This content is no longer accessible.', show_alert=True)
            return
        (_, author, body, scope, _) = post

        access_granted = False
        if mode == 'for':
            access_granted = call.from_user.username == author or call.from_user.username in scope.split(' ')
        elif mode == 'except':
            access_granted = call.from_user.username not in scope.split(' ')

        if access_granted:
            logger.info('#' + id + ': @' + call.from_user.username + ' - access granted')
            bot.answer_callback_query(call.id, text=body, show_alert=True)
        else:
            logger.info('#' + id + ': @' + call.from_user.username + ' - access denied')
            bot.answer_callback_query(call.id, text='You are not allowed to view this content.', show_alert=True)
    except Exception as e:
        logger.error(e)

@bot.inline_handler(lambda query: re.match(r'^.+ (@.+)$', query.query.replace('_', 'x')))
def query_hide(inline_query):
    try:
        r = re.compile(r'( @.+)+$')
        body = r.sub('', inline_query.query)
        targets = list(dict.fromkeys(inline_query.query[len(body) + 1:].split(' ')))
        if '' in targets: targets.remove('')

        execute_query("""
        INSERT INTO posts (author, content, scope)
        VALUES ('""" + inline_query.from_user.username + """', '""" + body + """', '""" + ' '.join(targets).replace('@', '') + """');
        """)
        row_id = str(cursor.lastrowid)
        logger.info('#' + row_id + ' has been created by @' + inline_query.from_user.username)

        formatted_scope = ', '.join(targets[:-1])
        if len(targets) > 1:
            formatted_scope += ' and ' + targets[-1]
        else:
            formatted_scope = targets[0]

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

def main_loop():
    bot.polling(True)
    while True:
        time.sleep(3)

if __name__ == '__main__':
    try:
        execute_query("""
            CREATE TABLE IF NOT EXISTS posts (
              id INTEGER PRIMARY KEY AUTOINCREMENT,
              author TEXT,
              content TEXT,
              scope TEXT,
              mode INTEGER);
              """)

        logger.info('Starting main_loop...')
        main_loop()
    except Exception as e:
        logger.error(e)
