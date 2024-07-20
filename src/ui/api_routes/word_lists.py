import flask

from ui.word_lists import get_word_lists
from utils.api_responses import create_successful_response


word_lists_blueprint = flask.Blueprint("word-lists", __name__, url_prefix="/word-lists")


@word_lists_blueprint.get("/")
def get_word_lists_for_ui():
    return create_successful_response(
        [vars(word_list) for word_list in get_word_lists()]
    )
