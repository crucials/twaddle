from threading import Thread

import eel

from word_counter import WordCounter, speech_transcriber
from utils.responses import create_error_response, create_successful_response
from ui.errors.detailed_error import DetailedError
from ui.errors.unexpected_error import UnexpectedError


counter: WordCounter | None = None

@eel.expose('startCounterFromMicrophone')
def start_counter_from_microphone(language: str,
                                  recording_device_index: int | None = None):
    global counter

    if counter and counter.running or counter and not speech_transcriber:
        return create_error_response(DetailedError('already-running-error',
                                                   'words counting process ' +
                                                   'was already started'))
    
    try:
        counter = WordCounter(language, recording_device_index)
        counting_thread = Thread(target=counter.start)
        counting_thread.start()

        return create_successful_response(None)
    except ValueError as value_error:
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
