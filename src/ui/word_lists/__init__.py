from ui.word_lists.english_filler_words import english_filler_words
from ui.word_lists.spanish_filler_words import spanish_filler_words


preset_lists = [english_filler_words, spanish_filler_words]


def get_word_lists():
    return preset_lists


class WordListNotFoundError(ValueError):
    pass


def get_words_from_word_list(word_list_name):
    if word_list_name is None:
        return None

    found_word_lists = [
        word_list for word_list in get_word_lists() if word_list.name == word_list_name
    ]

    if len(found_word_lists) < 1:
        raise WordListNotFoundError()

    return found_word_lists[0].words
