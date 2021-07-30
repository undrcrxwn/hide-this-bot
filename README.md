# Hide This Bot
[Hide This Bot](https://t.me/hidethisbot) is an inline Telegram bot to keep your private messages hidden from prying eyes.

[![](https://www.codefactor.io/repository/github/undrcrxwn/hidethisbot/badge/master)](https://www.codefactor.io/repository/github/undrcrxwn/hidethisbot/overview/master) 
[![](https://img.shields.io/badge/telegram-@hidethisbot-blue)](https://t.me/hidethisbot) 
[![](https://img.shields.io/badge/community-@hidethisbot__chat-blue)](https://t.me/hidethisbot_chat)

### How do I host it?
Here is a brief guide you can follow to host your own Hide This Bot in case you are afraid of data leaks or for any other reason.
1. Create a new bot via [Botfather](https://t.me/botfather).
2. Make your bot inline at Bot → Bot Settings → Inline Mode → Turn inline mode on.
3. Optionally set up your custom inline placeholder (e. g. <i>sample text @user</i>) at Bot → Bot Settings → Inline Mode → Edit inline placeholder.
5. [Fork](https://https://github.com/undrcrxwn/hidethisbot/fork) this repo.
6. [Deploy](https://heroku.com/deploy?template=https://github.com/undrcrxwn/hidethisbot) it to Heroku (recomended) or some other hosting.
7. Set up all required environment variables (aka config vars) at Heroku → Pipeline → App → Settings → Config Vars.

### Environment variables
- `API_TOKEN` – Telegram API bot token
- `LOG_PATH` – path to the log-file
- `DATABASE_URL` – URL of the PostgreSQL database

### Telegram input template
> @hidethisbot sample text @user1 @user2 @user3
- `@hidethisbot` – inline mention of the bot
- `sample text` – text to be hidden
- `@user1 @user2 @user3` – list of users in scope

### Available modes
- `for` – hidden content can only be seen by the author and users in scope
- `except` – hidden content can be seen by everyone except users in scope

### Placeholders
Can be used in messages as normal text. For instance, you can write the following message (using `except`-mode) in a public chat (everyone will see his own `full_name` instead of `{name}`):
> @hidethisbot I guess its time to kick {name} from this chat. cant stand this clown anymore @undrcrxwn
- `{username}` – viewer's username (e. g. **@undrcrxwn**)
- `{name}` – viewer's full name (e. g. **Big Floppa**)
- `{uid}` – viewer's UID (e. g. **id837151456**)
- `{lang}` – viewer's language code (e. g. **en** or **pt-br**)
- `{pid}` – post (DB row) ID (e. g. **#32400360**)
- `{ts}` – post creation timestamp (e. g. **2077-07-05 19:53:17.864156**)
- `{now}` – precise timestamp (e. g. **2077-07-05 19:53:17.864156**)
- `{date}` – current date (e. g. **2077-07-05**)
- `{time}` – current time (e. g. **19:53**)

All datetime-related placeholders depend on the server's timezone which can be changed by specifying optional `TZ` environment variable. Expected value is [TZ database name](https://en.wikipedia.org/wiki/List_of_tz_database_time_zones#List) (e. g. `	America/New_York` or `Europe/Moscow`).
