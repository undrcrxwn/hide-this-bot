class Locale():
    too_long_title: str
    for_title: str
    except_title: str
    spoiler_title: str

    too_long_message: str
    for_message: str
    except_message: str
    spoiler_message: str
    group_greeting_message: str
    info_message: str

    how_to_use: str
    too_long_description: str

    not_allowed: str
    not_accessible: str
    view: str
    and_connector: str

class LocalesDict:
    def __init__(self, locales, default_locale: Locale):
        self.locales = locales
        self.default_locale = default_locale

    def __getitem__(self, lang) -> Locale:
        if lang is None:
            return self.default_locale
        return self.locales.get(lang[:2], self.default_locale)
