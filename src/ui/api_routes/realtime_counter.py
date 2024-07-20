from threading import Thread

import flask
from werkzeug.exceptions import Conflict, BadRequest

from word_counters.realtime_word_counter import RealtimeWordCounter
from word_counters import WordCounter
from ui.word_lists import get_words_from_word_list, WordListNotFoundError
from utils.api_responses import create_successful_response


realtime_counter_blueprint = flask.Blueprint(
    "realtime-counter", __name__, url_prefix="/realtime-counter"
)

counter: RealtimeWordCounter | None = None


@realtime_counter_blueprint.post("/")
def start_counter_from_microphone():
    global counter

    request_body = flask.request.get_json()

    if not isinstance(request_body, dict):
        raise BadRequest(
            "request body must be a json object with optional "
            + "properties like 'language'"
        )

    # if counter initialized but the transcription model hasnt been loaded yet
    loading = counter and not WordCounter.speech_transcriber

    if counter and counter.running or loading:
        raise Conflict("words counting process was already started")
    try:
        words_to_count = get_words_from_word_list(request_body.get("word_list_name"))

        counter = RealtimeWordCounter(
            request_body.get("language"),
            request_body.get("recording_device_index"),
            words_to_count,
        )
        counting_thread = Thread(target=counter.start)
        counting_thread.start()
    except WordListNotFoundError as word_list_not_found_error:
        raise BadRequest(
            "specified word list doesn't exist"
        ) from word_list_not_found_error
    except ValueError as value_error:
        raise BadRequest("specified language is not supported") from value_error

    return create_successful_response()


@realtime_counter_blueprint.get("/result")
def get_counter_result():
    global counter

    if not counter or not counter.running:
        return BadRequest(
            "couldn't get the result," + "words counting process was not started"
        )

    spoken_words_stats = [
        {"word": word, "count": counter.words_count_values[word]}
        for word in counter.words_count_values
    ]

    return create_successful_response(
        {"full_text": counter.full_text, "words_stats": spoken_words_stats}
    )


@realtime_counter_blueprint.delete("/")
def reset_counter():
    global counter

    if not counter or not counter.running:
        return BadRequest(
            "words counting process was not started," + "so it can't be stopped"
        )
    counter.stop()
    counter = None

    return create_successful_response()
