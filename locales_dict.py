class Locale():
    too_long_message: str
    too_long_title: str
    too_long_description: str
    how_to_use: str
    for_message: str
    except_message: str
    for_title: str
    except_title: str
    and_connector: str
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
        if not lang: return self.default_locale
        return self.locales.get(lang[:2], self.default_locale)
