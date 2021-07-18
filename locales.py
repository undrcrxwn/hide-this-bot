from locales_dict import Locale

locale_en = Locale()
locale_ru = Locale()

# MESSAGE_TOO_LONG_MESSAGE
locale_en.message_too_long_message = '🥺 Sorry, your message can\'t be sent as it exceeds the limit of 200 characters.'
locale_ru.message_too_long_message = '🥺 Ваше сообщение не может быть отправлено, так как его длина превышает лимит в 200 символов.'

# MESSAGE_TOO_LONG_TITLE
locale_en.message_too_long_title = 'Your message is too long'
locale_ru.message_too_long_title = 'Слишком длинное сообщение'

# MESSAGE_TOO_LONG_DESCRIPTION
locale_en.message_too_long_description = 'Please shorten the length of your message so that it doesn\'t exceed the limit of 200 characters.'
locale_ru.message_too_long_description = 'Пожалуйста, сократите длину вашего сообщения, чтобы она не превышала лимит в 200 символов.'

# HOW_TO_USE
locale_en.how_to_use = 'How to use this bot?'
locale_ru.how_to_use = 'Как пользоваться этим ботом?'

# PRIVATE_MESSAGE_FOR
locale_en.private_message_for = 'Private message for %s.'
locale_ru.private_message_for = 'Приватное сообщение для %s.'

# PRIVATE_MESSAGE_EXCEPT
locale_en.private_message_except = 'Private message for everyone except %s.'
locale_ru.private_message_except = 'Приватное сообщение для всех, кроме %s.'

# FOR_TITLE
locale_en.for_title = 'For %s'
locale_ru.for_title = 'Для %s'

# EXCEPT_TITLE
locale_en.except_title = 'Except %s'
locale_ru.except_title = 'Кроме %s'

# VIEW
locale_en.view = 'View'
locale_ru.view = 'Открыть'

# NOT_ALLOWED
locale_en.not_allowed = 'You are not allowed to view this content.'
locale_ru.not_allowed = 'Вам запрещено просматривать этот контент.'

# NOT_ACCESSIBLE
locale_en.not_accessible = 'This content is no longer accessible.'
locale_ru.not_accessible = 'Этот контент больше недоступен.'

# GROUP_GREETING_MESSAGE
locale_en.group_greeting_message = (
        '👋 Hi! My name is %s and I can help you send private messages that only certain people can view. '
        'To learn more send /start@%s and feel free to ask for help in our '
        '<a href="t.me/hidethisbot_chat">public community</a> if you\'ve got any questions.')
locale_ru.group_greeting_message = (
        '👋 Привет! Меня зовут %s и я могу помочь вам отправлять сообщения, которые смогут прочитать только '
        'определённый круг лиц. Чтобы узнать больше отправьте команду /start@%s и не стесняйтесь просить о помощи '
        'в нашем <a href="t.me/hidethisbot_chat">публичном чате</a>, если у вас появятся какие-либо вопросы.')

# INFO_MESSAGE
locale_en.info_message = (
        'If you still have questions after reading the article, you can contact support or simply ask '
        'for help in our public chat at any time you want.\n\n'
        '👥 Public chat: @hidethisbot_chat\n'
        '⚙ Support: @undrcrxwn')
locale_ru.info_message = (
        'Если у вас остались вопросы после прочтения статьи, вы можете в любое время обратиться в службу '
        'поддержки или попросить о помощи в нашем публичном чате.\n\n'
        '👥 Публичный чат: @hidethisbot_chat\n'
        '⚙ Поддержка: @undrcrxwn')
