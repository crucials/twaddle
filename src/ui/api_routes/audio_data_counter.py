import flask


audio_data_word_counter_blueprint = flask.Blueprint(
    'audio-data-counter',
    __name__,
    url_prefix='/audio-data-counter'
)

@audio_data_word_counter_blueprint.post('/')
def start_audio_data_counter():
    pass
