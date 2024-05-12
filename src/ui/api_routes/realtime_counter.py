from threading import Thread

import flask
from werkzeug.exceptions import Conflict, BadRequest

from word_counters.realtime_word_counter import RealtimeWordCounter
from ui.word_lists import get_word_lists
from utils.api_responses import create_successful_response


realtime_counter_blueprint = flask.Blueprint('realtime-counter', __name__,
                                                   url_prefix='/realtime-counter')

counter: RealtimeWordCounter | None = None

def __get_words_from_word_list(word_list_name):
    if word_list_name == None:
        return None
    
    found_word_lists = [word_list for word_list in get_word_lists()
                        if word_list.name == word_list_name]
    
    if len(found_word_lists) < 1:
        raise BadRequest(f'word list with a name {word_list_name} doesnt exist')
    
    return found_word_lists[0].words

@realtime_counter_blueprint.post('/')
def start_counter_from_microphone(language: str | None = None,
                                  recording_device_index: int | None = None,
                                  word_list_name: str | None = None):
    global counter

    # if counter initialized but the transcription model hasnt been loaded yet
    loading = counter and not RealtimeWordCounter.speech_transcriber

    if counter and counter.running or loading:
        raise Conflict('words counting process was already started')
    try:
        words_to_count = __get_words_from_word_list(word_list_name)
        
        counter = RealtimeWordCounter(language, recording_device_index, words_to_count)
        counting_thread = Thread(target=counter.start, args=[1])
        counting_thread.start()
    except ValueError:
        raise BadRequest('specified language is not supported')
    
    return create_successful_response()

@realtime_counter_blueprint.get('/result')
def get_counter_result():
    global counter

    if not counter or not counter.running:
        return BadRequest('couldn\'t get the result,' +
                          'words counting process was not started')
    
    spoken_words_stats = [{'word': word,
                           'count': counter.words_count_values[word]}
                          for word
                          in counter.words_count_values]
    
    return create_successful_response({
        'full_text': counter.full_text,
        'words_stats': spoken_words_stats
    })

@realtime_counter_blueprint.delete('/')
def reset_counter():
    global counter

    if not counter or not counter.running:
        return BadRequest('words counting process was not started,' +
                          'so it can\'t be stopped')
    counter.stop()
    counter = None

    return create_successful_response()
