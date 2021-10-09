# Hide This Bot
[Hide This Bot](https://t.me/hidethisbot) is an inline Telegram bot to keep your private messages hidden from prying eyes.

[![](https://www.codefactor.io/repository/github/undrcrxwn/hidethisbot/badge/master)](https://www.codefactor.io/repository/github/undrcrxwn/hidethisbot/overview/master) 
[![](https://img.shields.io/badge/telegram-@hidethisbot-blue)](https://t.me/hidethisbot) 
[![](https://img.shields.io/badge/community-@hidethisbot__chat-blue)](https://t.me/hidethisbot_chat)
[![](https://i.imgur.com/gYCmw0k.png)](#)

### How do I host it?
Here is a brief guide you can follow to host your own Hide This Bot in case you are afraid of data leaks or for any other reason.
1. Create a new bot via [Botfather](https://t.me/botfather).
2. Make your bot inline at Bot → Bot Settings → Inline Mode → Turn inline mode on.
3. Optionally set up your custom inline placeholder (e. g. <i>sample text @user</i>) at Bot → Bot Settings → Inline Mode → Edit inline placeholder.
5. [Fork](https://github.com/undrcrxwn/hidethisbot/fork) this repo.
6. [Deploy](https://heroku.com/deploy?template=https://github.com/undrcrxwn/hidethisbot) it to Heroku (recomended) or some other hosting.
7. Set up all required environment variables (aka config vars) at Heroku → Pipeline → App → Settings → Config Vars.

### Environment variables
- `API_TOKEN` – Telegram API bot token
- `LOG_PATH` – path to the log-file (e. g. **logs/session_{time}.log**)
- `DATABASE_URL` – connection URL of the database (see [examples](https://www.prisma.io/docs/reference/database-reference/connection-urls))

### Telegram input template
> @hidethisbot sample text @user1 @user2 @user3
- `@hidethisbot` – inline mention of the bot
- `sample text` – text to be hidden
- `@user1 @user2 @user3` – list of users in scope

### Available modes
- `spoiler` – hidden content can be seen by everyone
- `for` – hidden content can only be seen by the author and users in scope
- `except` – hidden content can be seen by everyone except users in scope

### Placeholders
Can be used in messages to be replaced with user-related values. For instance, you can send the following message to a public chat to make everyone see his own `full_name` instead of `{name}` placeholder:
> @hidethisbot I guess its time to kick {name} from this chat. cant stand this clown anymore
- `{username}` – viewer's username (e. g. **@undrcrxwn**)
- `{uid}` – viewer's UID (e. g. **id837151456**)
- `{lang}` – viewer's language code (e. g. **en** or **pt-br**)
- `{pid}` – post (DB row) ID (e. g. **#32400360**)
- `{created}` – post creation timestamp (e. g. **2077-07-05 19:53:17.864156**)
- `{queries}` – total count of inline queries sent by viewer (e. g. **42**)
- `{first_interaction}` – precise UTC timestamp of when viewer was saved to the database for the first time (e. g. **2077-07-05 19:53:17.864156**)
- `{dialog}` – indicates whether viewer has ever written to the bot in private chat (e. g. **Yes**)
- `{utc}` – precise UTC timestamp (e. g. **2077-07-05 19:53:17.864156**)
- `{date}` – current UTC date (e. g. **2077-07-05**)
- `{time}` – current UTC time (e. g. **19:53**)
- `{name}` – viewer's full name (e. g. **Big Floppa**)
- `{first_name}` – viewer's first name (e. g. **Big**)
- `{last_name}` – viewer's last name (e. g. **Floppa**)

All datetime-related placeholders adhere to the UTC timezone with +00:00 shift.
