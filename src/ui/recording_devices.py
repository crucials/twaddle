import pyaudio
import flask
from werkzeug.exceptions import BadRequest


recording_devices = flask.Blueprint('recording-devices', __name__,
                                    url_prefix='/recording-devices')

@recording_devices.get('/')
def get_recording_devices():
    input_devices = []

    audio = None
    try:
        audio = pyaudio.PyAudio()
        for device_index in range(audio.get_device_count()):
            device = audio.get_device_info_by_index(device_index)

            if device['maxInputChannels'] > 1:
                input_devices.append(device)
    finally:
        if audio:
            audio.terminate()

    return input_devices
