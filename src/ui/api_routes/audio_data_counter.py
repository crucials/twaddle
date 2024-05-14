import time
import os

import flask
from werkzeug.exceptions import BadRequest, Conflict

from utils.api_responses import create_successful_response
from word_counters.file_word_counter import FileWordCounter
from word_counters import WordCounter


audio_data_word_counter_blueprint = flask.Blueprint(
    'audio-data-counter',
    __name__,
    url_prefix='/audio-data-counter'
)

counter: FileWordCounter | None = None

@audio_data_word_counter_blueprint.post('/')
def start_audio_data_counter():
    global counter

    SUPPORTED_TYPES_EXTENSIONS = {
        'audio/mpeg': 'mp3',
        'audio/wav': 'wav',
        'audio/wave': 'wav',
    }

    audio_file = flask.request.files.get('audio_file')

    if audio_file == None:
        raise BadRequest('request must contain multipart form data ' +
                         'with \'audio_file\' field')

    if audio_file.mimetype not in SUPPORTED_TYPES_EXTENSIONS:
        raise BadRequest('file audio type is not supported. only these ' +
                         'can be transcribed: ' +
                         ', '.join(SUPPORTED_TYPES_EXTENSIONS))
    
    # if counter initialized but the transcription model hasnt been loaded yet
    loading = counter and not WordCounter.speech_transcriber

    if counter and counter.running or loading:
        raise Conflict('words counting process was already started')
    
    extension = SUPPORTED_TYPES_EXTENSIONS[audio_file.mimetype]
    temp_audio_file_path = f'./{time.time()}.{extension}'
    audio_file.save(temp_audio_file_path)

    try:
        counter = FileWordCounter(temp_audio_file_path,
                                  flask.request.form.get('language'),
                                  None)
        
        counter.start()
        
        spoken_words_stats = [{'word': word,
                               'count': counter.words_count_values[word]} 
                               for word in counter.words_count_values]
        
        return create_successful_response({
            'full_text': counter.full_text,
            'words_stats': spoken_words_stats
        })
    except ValueError:
        raise BadRequest('specified language is not supported')
    except Exception as error:
        raise error
    finally:
        os.remove(temp_audio_file_path)
