import sys
import platform

import eel
import eel.browsers

from utils.create_path_from_executable import create_path_from_executable
from ui.count_from_microphone import start_counter_from_microphone, reset_counter
from ui.get_recording_devices import get_recording_devices
from ui.word_lists.get_word_lists import get_word_lists_for_ui


def stop(route, websockets):
    print('exiting')
    reset_counter()

    sys.exit(0)

print('launching')

operating_system = platform.system()
if operating_system == 'Linux':
    eel.browsers.set_path('chrome', create_path_from_executable('ui', 'bin', 'ungoogled-chromium.AppImage'))
elif operating_system == 'Windows':
    eel.browsers.set_path('chrome', create_path_from_executable('ui', 'bin','ungoogled-chromium.exe'))
else:
    raise Exception(f'your os is not supported ({operating_system}), ' +
                    'this app is available only for linux and windows')

eel.init('src/ui/web/dist')
eel.start('index.html', mode = 'chrome', size = ( 1400, 750 ), close_callback=stop)
