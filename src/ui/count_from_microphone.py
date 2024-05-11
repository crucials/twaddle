from threading import Thread

import eel

from word_counters.realtime_word_counter import RealtimeWordCounter
from utils.responses import create_error_response, create_successful_response
from ui.errors.detailed_error import DetailedError
from ui.errors.unexpected_error import UnexpectedError
from ui.word_lists.get_word_lists import get_word_lists


counter: RealtimeWordCounter | None = None

def __get_words_from_word_list(word_list_name):
    if word_list_name == None:
        return None
    
    found_word_lists = [word_list for word_list in get_word_lists()
                        if word_list.name == word_list_name]
    
    if len(found_word_lists) < 1:
        raise DetailedError('word-list-not-found-error', 'word list with a name ' +
                            f'{word_list_name} doesnt exist')
    
    return found_word_lists[0].words

@eel.expose('startCounterFromMicrophone')
def start_counter_from_microphone(language: str | None = None,
                                  recording_device_index: int | None = None,
                                  word_list_name: str | None = None):
    global counter

    # if counter initialized but the transcription model hasnt been loaded yet
    loading = counter and not RealtimeWordCounter.speech_transcriber

    if counter and counter.running or loading:
        return create_error_response(DetailedError('already-running-error',
                                                   'words counting process ' +
                                                   'was already started'))
    
    try:
        words_to_count = __get_words_from_word_list(word_list_name)
        
        counter = RealtimeWordCounter(language, recording_device_index, words_to_count)
        counting_thread = Thread(target=counter.start, args=[1])
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
    
    return create_successful_response({
        'full_text': counter.full_text,
        'words_stats': spoken_words_stats
    })

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
