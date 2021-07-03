# Hide This Bot
[Hide This Bot](https://t.me/hidethisbot) is an inline Telegram bot to keep your private messages hidden from prying eyes.


#### Environment variables:
- `API_TOKEN` – Telegram API bot token
- `LOG_PATH` – path to the log-file
- `DATABASE_URL` – URL of the PostgreSQL database


#### Available modes:
- `for` – hidden content can only be seen by the author and users in scope
- `except` – hidden content can be seen by everyone except users in scope

#### Telegram input template:
> @hidethisbot sample text @user1 @user2 @user3
- `@hidethisbot` – inline mention of the bot
- `sample text` – text to be hidden
- `@user1 @user2 @user3` – list of users in scope

### [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/undrcrxwn/hidethisbot)
