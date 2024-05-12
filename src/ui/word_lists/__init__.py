from ui.word_lists.english_filler_words import english_filler_words
from ui.word_lists.spanish_filler_words import spanish_filler_words


preset_lists = [english_filler_words, spanish_filler_words]

def get_word_lists():
    return preset_lists
