from threading import Thread

import eel

from word_counter import WordCounter
from utils.responses import create_error_response, create_successful_response
from ui.errors.detailed_error import DetailedError


counter: WordCounter | None = None

@eel.expose('startCounterFromMicrophone')
def start_counter_from_microphone():
    global counter

    if counter and counter.running:
        return create_error_response(DetailedError('already-running-error',
                                                   'words counting process ' +
                                                   'was already started'))
    
    try:
        counter = WordCounter()
        counting_thread = Thread(target=counter.start, args=['en'])
        counting_thread.start()

        return create_successful_response(None)
    except Exception as error:
        return create_error_response(error)

@eel.expose('stopCounterFromMicrophone')
def stop_counter_from_microphone():
    global counter

    if not counter or not counter.running:
        return create_error_response(DetailedError('counter-not-running-error',
                                                   'words counting process ',
                                                   'was not started'))

    try:
        counter.stop()

        return create_successful_response(counter.words_count_values)
    except Exception as error:
        return create_error_response(error)
