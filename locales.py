from locales_dict import Locale, LocalesDict

locale_en = Locale()
locale_ru = Locale()
locale_uk = Locale()
locale_de = Locale()
locale_it = Locale()
locale_pt = Locale()

locales = LocalesDict({
    'en': locale_en,
    'ru': locale_ru,
    'uk': locale_uk,
    'de': locale_de,
    'it': locale_it,
    'pt': locale_pt
}, locale_en)

# TOO_LONG_TITLE
locale_en.too_long_title = 'Your message is too long'
locale_ru.too_long_title = 'Слишком длинное сообщение'
locale_uk.too_long_title = 'Занадто довге повідомлення'
locale_de.too_long_title = 'Deine Nachricht ist zu lang'
locale_it.too_long_title = 'Il tuo messaggio è troppo lungo'
locale_pt.too_long_title = 'Sua mensagem é muito longa'

# FOR_TITLE
locale_en.for_title = 'For %s'
locale_ru.for_title = 'Для %s'
locale_uk.for_title = 'Для %s'
locale_de.for_title = 'Für %s'
locale_it.for_title = 'Per %s'
locale_pt.for_title = 'Para %s'

# EXCEPT_TITLE
locale_en.except_title = 'Except %s'
locale_ru.except_title = 'Кроме %s'
locale_uk.except_title = 'Крім %s'
locale_de.except_title = 'Akzeptiere %s'
locale_it.except_title = 'Tranne %s'
locale_pt.except_title = 'Exceto %s'

# SPOILER_TITLE
locale_en.spoiler_title = 'Spoiler'
locale_ru.spoiler_title = 'Спойлер'
locale_uk.spoiler_title = 'Спойлер'
locale_de.spoiler_title = 'Spoiler'
locale_it.spoiler_title = 'Spoiler'
locale_pt.spoiler_title = 'Spoiler'


# TOO_LONG_MESSAGE
locale_en.too_long_message = '🥺 Sorry, your message can\'t be sent as it exceeds the limit of 200 characters.'
locale_ru.too_long_message = '🥺 Ваше сообщение не может быть отправлено, так как его длина превышает лимит в 200 символов.'
locale_uk.too_long_message = '🥺 Ваше повідомлення не може бути відправлено, так як його довжина перевищує ліміт в 200 символів.'
locale_de.too_long_message = '🥺 Sorry, deine Nachricht kann nicht gesendet werden, da sie das Limit von 200 Zeichen überschreitet.'
locale_it.too_long_message = '🥺 Mi dispiace, il tuo messaggio non può essere mandato, supera il limite di 200 caratteri.'
locale_pt.too_long_message = '🥺 Desculpe, sua mensagem não pode ser enviada, pois excede o limite de 200 caracteres.'

# FOR_MESSAGE
locale_en.for_message = 'Private message for %s.'
locale_ru.for_message = 'Приватное сообщение для %s.'
locale_uk.for_message = 'Приватне повідомлення для %s.'
locale_de.for_message = 'Private Nachricht für %s.'
locale_it.for_message = 'Messaggio privato per %s.'
locale_pt.for_message = 'Mensagem privada para %s.'

# EXCEPT_MESSAGE
locale_en.except_message = 'Private message for everyone except %s.'
locale_ru.except_message = 'Приватное сообщение для всех, кроме %s.'
locale_uk.except_message = 'Приватне повідомлення для всіх, крім %s.'
locale_de.except_message = 'Private Nachricht an alle außer %s.'
locale_it.except_message = 'Messaggio privato per tutti tranne %s.'
locale_pt.except_message = 'Mensagem privada para todos, exceto %s.'

# SPOILER_MESSAGE
locale_en.spoiler_message = 'Public spoiler message.'
locale_ru.spoiler_message = 'Публичное сообщение под спойлером.'
locale_uk.spoiler_message = 'Публічне повідомлення під спойлером.'
locale_de.spoiler_message = 'Öffentlicher Spoiler für alle:'
locale_it.spoiler_message = 'Messaggio contenente spoiler.'
locale_pt.spoiler_message = 'Mensagem pública de spoiler.'

# GROUP_GREETING_MESSAGE
locale_en.group_greeting_message = (
        '👋 Hi! My name is %s and I can help you send private messages that only certain people can view. '
        'To learn more send /start@%s and feel free to ask for help in our '
        '<a href="t.me/radzinsky_chat">public community</a> if you\'ve got any questions.')
locale_ru.group_greeting_message = (
        '👋 Привет! Меня зовут %s и я могу помочь вам отправлять сообщения, которые смогут прочитать только '
        'определённый круг лиц. Чтобы узнать больше отправьте команду /start@%s и не стесняйтесь просить о помощи '
        'в нашем <a href="t.me/radzinsky_chat">публичном чате</a>, если у вас появятся какие-либо вопросы.')
locale_uk.group_greeting_message = (
        '👋 Привіт! Мене звуть %s і я можу допомогти вам відправляти повідомлення, які зможуть прочитати тільки '
        'певне коло осіб. Щоб дізнатися більше відправте команду /start@%s і не соромтеся просити про допомогу '
        'в нашому <a href="t.me/radzinsky_chat">публічному чаті</a>, якщо у вас виникнуть будь-які питання.')
locale_de.group_greeting_message = (
        '👋 Hi! Mein Name ist %s und ich kann dir helfen, private Nachrichten zu verschicken, die nur bestimmte Personen sehen können. '
        'Um zu sehen, wie das geht, sende einfach /start@%s! Fühle dich frei, bei Fragen, in unserer '
        '<a href="t.me/radzinsky_chat">Support Gruppe</a> zu fragen.')
locale_it.group_greeting_message = (
        '👋 Ciao! Il mio nome è %s E posso aiutarti ad inviare messaggi privati che solo alcuni possono vedere. '
        'per sapere di più invia /start@%s e sentiti libero di chiedere aiuto '
        '<a href="t.me/radzinsky_chat">gruppo pubblico</a> se hai domande.')
locale_pt.group_greeting_message = (
        '👋 Oi! Meu nome é %s e posso ajudá-lo a enviar mensagens privadas que apenas algumas pessoas podem ver. '
        'Para saber mais envie /start@%s e sinta-se livre para pedir ajuda em nosso '
        '<a href="t.me/radzinsky_chat">grupo público</a> se você tiver alguma dúvida.')

# INFO_MESSAGE
locale_en.info_message = (
        'If you still have questions after reading the article, you can contact support or simply ask '
        'for help in our public chat at any time you want.\n\n'
        '👥 Public chat: @radzinsky_chat\n'
        '⚙ Support: @undrcrxwn')
locale_ru.info_message = (
        'Если у вас остались вопросы после прочтения статьи, вы можете в любое время обратиться в '
        'поддержку или попросить о помощи в нашем публичном чате.\n\n'
        '👥 Публичный чат: @radzinsky_chat\n'
        '⚙ Поддержка: @undrcrxwn')
locale_uk.info_message = (
        'Якщо у вас залишилися питання після прочитання статті, ви можете в будь-який час звернутися в службу '
        'підтримки або попросити про допомогу в нашому публічному чаті.\n\n'
        '👥 Публічний чат: @radzinsky_chat\n'
        '⚙ Підтримка: @undrcrxwn')
locale_de.info_message = (
        'Wenn du nach dem Lesen des Artikels noch Fragen hast, kannst du den Support kontaktieren oder einfach '
        'in unserem öffentlichen Chat um Hilfe bitten, wann immer du willst.\n\n'
        '👥 öffentlichen Chat: @radzinsky_chat\n'
        '⚙ Hilfe: @undrcrxwn')
locale_it.info_message = (
         'Se hai ancora domande dopo aver letto questo articolo, puoi contattare il supporto nella nostra '
         'chat pubblica quando vuoi.\n\n'
         '👥 Gruppo pubblico: @radzinsky_chat\n'
         '⚙ Supporto: @undrcrxwn')
locale_pt.info_message = (
        'Se você ainda tiver dúvidas depois de ler o artigo, entre em contato com o suporte ou simplesmente pergunte '
        'para obter ajuda em nosso chat público a qualquer hora que você quiser.\n\n'
        '👥 Grupo público: @radzinsky_chat\n'
        '⚙ Suporte: @undrcrxwn')

# HOW_TO_USE
locale_en.how_to_use = 'How to use this bot?'
locale_ru.how_to_use = 'Как пользоваться этим ботом?'
locale_uk.how_to_use = 'Як користуватися цим ботом?'
locale_de.how_to_use = 'Wie geht das?'
locale_it.how_to_use = 'Come usare questo bot?'
locale_pt.how_to_use = 'Como usar este bot?'

# TOO_LONG_DESCRIPTION
locale_en.too_long_description = 'Please shorten the length of your message so that it doesn\'t exceed the limit of 200 characters.'
locale_ru.too_long_description = 'Пожалуйста, сократите длину вашего сообщения, чтобы она не превышала лимит в 200 символов.'
locale_uk.too_long_description = 'Будь ласка, скоротіть довжину Вашого повідомлення, щоб вона не перевищувала ліміт в 200 символів.'
locale_de.too_long_description = 'Bitte fasse dich etwas kürzer und überschreite das Limit von 200 Zeichen nicht.'
locale_it.too_long_description = 'Perfavore accorcia la lunghezza del tuo messaggio in modo che non superi i 200 caratteri.'
locale_pt.too_long_description = 'Por favor, reduza o tamanho da sua mensagem para que ela não exceda o limite de 200 caracteres.'


# NOT_ALLOWED
locale_en.not_allowed = 'You are not allowed to view this content.'
locale_ru.not_allowed = 'Вам запрещено просматривать этот контент.'
locale_uk.not_allowed = 'Вам заборонено переглядати цей контент.'
locale_de.not_allowed = 'Dir ist nicht gestattet, diesen Inhalt zu lesen.'
locale_it.not_allowed = 'Non hai il permesso per vedere questo messaggio.'
locale_pt.not_allowed = 'Você não tem permissão para visualizar este conteúdo.'

# NOT_ACCESSIBLE
locale_en.not_accessible = 'This content is no longer accessible.'
locale_ru.not_accessible = 'Этот контент больше недоступен.'
locale_uk.not_accessible = 'Цей контент більше недоступний.'
locale_de.not_accessible = 'Der Inhalt ist nicht mehr sichtbar.'
locale_it.not_accessible = 'Questo contenuto non è più accessibile.'
locale_pt.not_accessible = 'Este conteúdo não está mais acessível.'


# VIEW
locale_en.view = 'View'
locale_ru.view = 'Открыть'
locale_uk.view = 'Відкрити'
locale_de.view = 'Ansehen'
locale_it.view = 'Vedi'
locale_pt.view = 'Ver'

# AND_CONNECTOR
locale_en.and_connector = 'and'
locale_ru.and_connector = 'и'
locale_uk.and_connector = 'i'
locale_de.and_connector = '&'
locale_it.and_connector = 'e'
locale_pt.and_connector = 'e'

