# Hide This Bot
[Hide This Bot](https://t.me/hidethisbot) is an inline Telegram bot to keep your private messages hidden from prying eyes.

#### Environment variables
- `API_TOKEN` – Telegram API bot token
- `LOG_PATH` – path to the log-file
- `DATABASE_URL` – URL of the PostgreSQL database
- `TRACKING_CHAT_ID` – ID of the chat to be used for tracking /start messages, optional _(temporary solution that will be changed in future)_

#### Telegram input template
> @hidethisbot sample text @user1 @user2 @user3
- `@hidethisbot` – inline mention of the bot
- `sample text` – text to be hidden
- `@user1 @user2 @user3` – list of users in scope

#### Placeholders
Can be used in messages as normal text. For instance, you can write the following message (using `except`-mode) in a public chat (everyone will see his own name instead of `{name}`):
> @hidethisbot I guess its time to kick {name} from this chat. cant stand this clown anymore @undrcrxwn
- `{username}` – viewer's username (e. g. **@undrcrxwn**)
- `{name}` – viewer's full name (e. g. **Big Floppa**)
- `{uid}` – viewer's UID (e. g. **id837151456**)
- `{pid}` – post (DB row) ID (e. g. **#32400360**)
- `{time}` – precise timestamp (e. g. **2077-07-05 19:53:17.864156**)

#### Available modes
- `for` – hidden content can only be seen by the author and users in scope
- `except` – hidden content can be seen by everyone except users in scope

### [![Deploy](https://www.herokucdn.com/deploy/button.svg)](https://heroku.com/deploy?template=https://github.com/undrcrxwn/hidethisbot)
