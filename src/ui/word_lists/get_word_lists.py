import eel

from ui.word_lists.english_filler_words import english_filler_words
from ui.word_lists.spanish_filler_words import spanish_filler_words
from utils.responses import create_successful_response


preset_lists = [english_filler_words, spanish_filler_words]
 
def get_word_lists():
    return preset_lists

@eel.expose('getWordLists')
def get_word_lists_for_ui():
    return create_successful_response([vars(word_list) for word_list in get_word_lists()])
