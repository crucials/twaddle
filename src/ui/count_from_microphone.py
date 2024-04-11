from threading import Thread

import eel

from word_counter import WordCounter, speech_transcriber
from utils.responses import create_error_response, create_successful_response
from ui.errors.detailed_error import DetailedError
from ui.errors.unexpected_error import UnexpectedError
from ui.word_lists.get_word_lists import get_word_lists


counter: WordCounter | None = None

def __get_word_list_words(word_list_name):
    if word_list_name == None:
        return None
    
    found_word_lists = [word_list for word_list in get_word_lists()
                        if word_list.name == word_list_name]
    
    if len(found_word_lists) < 1:
        raise DetailedError('word-list-not-found-error', 'word list with a name ' +
                            f'{word_list_name} doesnt exist')
    
    return found_word_lists[0].words

@eel.expose('startCounterFromMicrophone')
def start_counter_from_microphone(language: str,
                                  recording_device_index: int | None = None,
                                  word_list_name: str | None = None):
    global counter

    if counter and counter.running or counter and not speech_transcriber:
        return create_error_response(DetailedError('already-running-error',
                                                   'words counting process ' +
                                                   'was already started'))
    
    try:
        words_to_count = __get_word_list_words(word_list_name)
        
        counter = WordCounter(language, recording_device_index, words_to_count)
        counting_thread = Thread(target=counter.start)
        counting_thread.start()

        return create_successful_response(None)
    except DetailedError as detailed_error:
        return create_error_response(detailed_error)
    except ValueError:
        return create_error_response(DetailedError('language-not-supported-error',
                                                   'selected language is not supported'))
    except Exception as error:
        return create_error_response(UnexpectedError(error))

@eel.expose('getCounterResult')
def get_counter_result():
    global counter

    if not counter or not counter.running:
        return create_error_response(DetailedError('counter-not-running-error',
                                                   'words counting process ' +
                                                   'was not started'))
    
    spoken_words_stats = [{'word': word,
                           'count': counter.words_count_values[word]}
                          for word
                          in counter.words_count_values]
    
    return create_successful_response(spoken_words_stats)

@eel.expose('resetCounter')
def reset_counter():
    global counter

    if not counter or not counter.running:
        return create_error_response(DetailedError('counter-not-running-error',
                                                   'words counting process ' +
                                                   'was not started'))

    try:
        counter.stop()
        result = counter.words_count_values
        counter = None

        return create_successful_response(result)
    except Exception as error:
        return create_error_response(UnexpectedError(error))
