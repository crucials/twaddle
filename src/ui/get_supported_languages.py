import eel

from supported_languages import languages


@eel.expose('getSupportedLanguages')
def get_supported_languages():
    return languages
