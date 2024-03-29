from threading import Thread
import time

import eel

from word_counter import start_counting, stop_counting, counter_running, words_count_values
from utils.responses import create_error_response, create_successful_response
from errors.detailed_error import DetailedError


@eel.expose('startCounterFromMicrophone')
def start_counter_from_microphone():
    if counter_running:
        return create_error_response(DetailedError('already-running-error',
                                                   'words counting process ' +
                                                   'was already started'))

    counting_thread = Thread(target=lambda: start_counting('en'))
    counting_thread.start()

    return create_successful_response(None)

@eel.expose('stopCounterFromMicrophone')
def stop_counter_from_microphone():
    if not counter_running:
        return create_error_response(DetailedError('counter-not-running-error',
                                                   'words counting process ',
                                                   'was not started'))

    stop_counting()
    return create_successful_response(words_count_values)
