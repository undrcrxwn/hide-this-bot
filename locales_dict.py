class Locale():
    message_too_long_message: str
    message_too_long_title: str
    message_too_long_description: str
    how_to_use: str
    private_message_for: str
    private_message_except: str
    for_title: str
    except_title: str
    view: str
    not_allowed: str
    not_accessible: str
    group_greeting_message: str
    info_message: str

class LocalesDict:
    def __init__(self, locales: dict[str, Locale], default_locale: Locale):
        self.locales = locales
        self.default_locale = default_locale

    def __getitem__(self, lang) -> Locale:
        return self.locales.get(lang, self.default_locale)
