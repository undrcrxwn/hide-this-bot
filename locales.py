from locales_dict import Locale

locale_en = Locale()
locale_ru = Locale()
locale_ua = Locale()
locale_it = Locale()

# TOO_LONG_MESSAGE
locale_en.too_long_message = '🥺 Sorry, your message can\'t be sent as it exceeds the limit of 200 characters.'
locale_ru.too_long_message = '🥺 Ваше сообщение не может быть отправлено, так как его длина превышает лимит в 200 символов.'
locale_ua.too_long_message = '🥺 Ваше повідомлення не може бути відправлено, так як його довжина перевищує ліміт в 200 символів.'
locale_it.too_long_message = '🥺 Mi dispiace, il tuo messaggio non può essere mandato, supera il limite di 200 caratteri.'

# TOO_LONG_TITLE
locale_en.too_long_title = 'Your message is too long'
locale_ru.too_long_title = 'Слишком длинное сообщение'
locale_ua.too_long_message = 'Занадто довге повідомлення'
locale_it.too_long_message = 'Il tuo messaggio è troppo lungo'

# TOO_LONG_DESCRIPTION
locale_en.too_long_description = 'Please shorten the length of your message so that it doesn\'t exceed the limit of 200 characters.'
locale_ru.too_long_description = 'Пожалуйста, сократите длину вашего сообщения, чтобы она не превышала лимит в 200 символов.'
locale_ua.too_long_description = 'Будь ласка, скоротіть довжину Вашого повідомлення, щоб вона не перевищувала ліміт в 200 символів.'
locale_it.too_long_description = 'Perfavore accorcia la lunghezza del tuo messaggio in modo che non superi i 200 caratteri.'

# HOW_TO_USE
locale_en.how_to_use = 'How to use this bot?'
locale_ru.how_to_use = 'Как пользоваться этим ботом?'
locale_ua.how_to_use = 'Як користуватися цим ботом?'
locale_it.how_to_use = 'Come usare questo bot?'

# FOR_MESSAGE
locale_en.for_message = 'Private message for %s.'
locale_ru.for_message = 'Приватное сообщение для %s.'
locale_ua.for_message = 'Приватне повідомлення для %s.'
locale_it.for_message = 'Messaggio privato per %s.'

# EXCEPT_MESSAGE
locale_en.except_message = 'Private message for everyone except %s.'
locale_ru.except_message = 'Приватное сообщение для всех,\n кроме %s.'
locale_ua.except_message = 'Приватне повідомлення для всіх,\n крім %s.'
locale_it.except_message = 'Messaggio privato per tutti tranne %s.'

# FOR_TITLE
locale_en.for_title = 'For %s'
locale_ru.for_title = 'Для %s'
locale_ua.for_title = 'Для %s'
locale_it.for_title = 'Per %s'

# EXCEPT_TITLE
locale_en.except_title = 'Except %s'
locale_ru.except_title = 'Кроме %s'
locale_ua.except_title = 'Крім %s'
locale_it.except_title = 'Tranne %s'

# AND_CONNECTOR
locale_en.and_connector = 'and'
locale_ru.and_connector = 'и'
locale_ua.and_connector = 'i'
locale_it.and_connector = 'e'

# VIEW
locale_en.view = 'View'
locale_ru.view = 'Открыть'
locale_ua.view = 'Відкрити'
locale_it.view = 'Vedi'

# NOT_ALLOWED
locale_en.not_allowed = 'You are not allowed to view this content.'
locale_ru.not_allowed = 'Вам запрещено просматривать этот контент.'
locale_ua.not_allowed = 'Вам заборонено переглядати цей контент.'
locale_it.not_allowed = 'Non hai il permesso per vedere questo messaggio.'

# NOT_ACCESSIBLE
locale_en.not_accessible = 'This content is no longer accessible.'
locale_ru.not_accessible = 'Этот контент больше недоступен.'
locale_ua.not_accessible = 'Цей контент більше недоступний.'
locale_it.not_accessible = 'Questo contenuto non è più accessibile.'

# GROUP_GREETING_MESSAGE
locale_en.group_greeting_message = (
        '👋 Hi! My name is %s and I can help you send private messages that only certain people can view. '
        'To learn more send /start@%s and feel free to ask for help in our '
        '<a href="t.me/hidethisbot_chat">public community</a> if you\'ve got any questions.')
locale_ru.group_greeting_message = (
        '👋 Привет! Меня зовут %s и я могу помочь вам отправлять сообщения, которые смогут прочитать только '
        'определённый круг лиц. Чтобы узнать больше отправьте команду /start@%s и не стесняйтесь просить о помощи '
        'в нашем <a href="t.me/hidethisbot_chat">публичном чате</a>, если у вас появятся какие-либо вопросы.')
locale_ua.group_greeting_message = (
        '👋 Привіт! Мене звуть %s і я можу допомогти вам відправляти повідомлення, які зможуть прочитати тільки '
        'певне коло осіб. Щоб дізнатися більше відправте команду /start@%s і не соромтеся просити про допомогу '
        'в нашому <a href="t.me/hidethisbot_chat">публічному чаті</a>, якщо у вас виникнуть будь-які питання.')
locale_it.group_greeting_message = (
        '👋 Ciao! Il mio nome è %s E posso aiutarti ad inviare messaggi privati che solo alcuni possono vedere. '
        'per sapere di più invia /start@%s e sentiti libero di chiedere aiuto '
        '<a href="t.me/hidethisbot_chat">gruppo pubblico</a> se hai domande.')

# INFO_MESSAGE
locale_en.info_message = (
        'If you still have questions after reading the article, you can contact support or simply ask '
        'for help in our public chat at any time you want.\n\n'
        '👥 Public chat: @hidethisbot_chat\n'
        '⚙ Support: @undrcrxwn')
locale_ru.info_message = (
        'Если у вас остались вопросы после прочтения статьи, вы можете в любое время обратиться в '
        'поддержку или попросить о помощи в нашем публичном чате.\n\n'
        '👥 Публичный чат: @hidethisbot_chat\n'
        '⚙ Поддержка: @undrcrxwn')
locale_ua.info_message = (
        'Якщо у вас залишилися питання після прочитання статті, ви можете в будь-який час звернутися в службу '
        'підтримки або попросити про допомогу в нашому публічному чаті.\n\n'
        '👥 Публічний чат: @hidethisbot_chat\n'
        '⚙ Підтримка: @undrcrxwn')
locale_it.info_message = (
         'Se hai ancora domande dopo aver letto questo articolo, puoi contattare il supporto nella nostra '
         'chat pubblica quando vuoi.\n\n'
         '👥 Gruppo pubblico: @hidethisbot_chat\n'
         '⚙ Supporto: @undrcrxwn')
