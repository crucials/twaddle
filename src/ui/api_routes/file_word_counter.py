import time
import os

import pyaudio
import flask
from werkzeug.exceptions import BadRequest, Conflict

from utils.api_responses import create_successful_response
from word_counters.file_word_counter import FileWordCounter
from word_counters import WordCounter
from ui.word_lists import WordListNotFoundError, get_words_from_word_list


audio_data_word_counter_blueprint = flask.Blueprint(
    "audio-file-word-counter", __name__, url_prefix="/audio-file-word-counter"
)

counter: FileWordCounter | None = None


@audio_data_word_counter_blueprint.post("/")
def start_audio_data_counter():
    global counter

    SUPPORTED_TYPES_EXTENSIONS = {
        "audio/mpeg": "mp3",
        "audio/wav": "wav",
        "audio/wave": "wav",
    }

    audio_file = flask.request.files.get("audio_file")
    request_form_data = flask.request.form

    if audio_file is None:
        raise BadRequest(
            "request must contain multipart form data " + "with 'audio_file' field"
        )

    if audio_file.mimetype not in SUPPORTED_TYPES_EXTENSIONS:
        raise BadRequest(
            "file audio type is not supported. only these "
            + "can be transcribed: "
            + ", ".join(SUPPORTED_TYPES_EXTENSIONS)
        )

    # if counter initialized but the transcription model hasnt been loaded yet
    loading = counter and not WordCounter.speech_transcriber

    if counter or loading:
        raise Conflict("words counting process was already started")

    extension = SUPPORTED_TYPES_EXTENSIONS[audio_file.mimetype]
    temp_audio_file_path = f"./{time.time()}.{extension}"
    audio_file.save(temp_audio_file_path)

    try:
        words_to_count = get_words_from_word_list(
            request_form_data.get("word_list_name")
        )
        counter = FileWordCounter(
            temp_audio_file_path, request_form_data.get("language"), words_to_count
        )

        counter.start()

        spoken_words_stats = [
            {"word": word, "count": counter.words_count_values[word]}
            for word in counter.words_count_values
        ]

        return create_successful_response(
            {
                "full_text": counter.full_text,
                "words_stats": spoken_words_stats,
                "audio_file_seconds_duration": counter.audio_file_seconds_duration,
            }
        )
    except WordListNotFoundError as word_list_not_found_error:
        raise BadRequest(
            "specified word list doesn't exist"
        ) from word_list_not_found_error
    except ValueError as value_error:
        raise BadRequest("specified language is not supported") from value_error
    except Exception as error:
        raise error
    finally:
        os.remove(temp_audio_file_path)


# def get_audio_file_length(file: ):

