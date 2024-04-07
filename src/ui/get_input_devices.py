import pyaudio
import eel

from ui.errors.unexpected_error import UnexpectedError
from utils.responses import create_error_response, create_successful_response


@eel.expose('getInputDevices')
def get_input_devices():
    input_devices = []

    audio = None
    try:
        audio = pyaudio.PyAudio()
        for device_index in range(audio.get_device_count()):
            device = audio.get_device_info_by_index(device_index)

            if device['maxInputChannels'] > 0:
                input_devices.append(device)
    except Exception as error:
        return create_error_response(UnexpectedError(error))
    finally:
        if audio:
            audio.terminate()

    return create_successful_response(input_devices)
