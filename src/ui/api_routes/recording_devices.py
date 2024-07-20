import pyaudio
import flask

from utils.api_responses import create_successful_response


recording_devices_blueprint = flask.Blueprint(
    "recording-devices", __name__, url_prefix="/recording-devices"
)


@recording_devices_blueprint.get("/")
def get_recording_devices():
    input_devices = []

    audio = None
    try:
        audio = pyaudio.PyAudio()
        for device_index in range(audio.get_device_count()):
            device = audio.get_device_info_by_index(device_index)

            if int(device["maxInputChannels"]) > 1:
                input_devices.append(device)
    finally:
        if audio:
            audio.terminate()

    return create_successful_response(input_devices)
