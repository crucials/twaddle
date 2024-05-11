import sys
import os
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

path_to_linux_chromium = create_path_from_executable('ui', 'bin', 'ungoogled-chromium.AppImage')
path_to_windows_chromium = create_path_from_executable('ui', 'bin', 'ungoogled-chromium.exe')

operating_system = platform.system()
if operating_system == 'Linux' and os.path.isfile(path_to_linux_chromium):
    eel.browsers.set_path('chrome', path_to_linux_chromium)
elif operating_system == 'Windows' and os.path.isfile(path_to_windows_chromium):
    eel.browsers.set_path('chrome', path_to_windows_chromium)
else:
    print('failed to load a built-in ungoogled chromium, using the default chrome browser')

eel.init('src/ui/electron/dist')
eel.start('index.html', mode = 'chrome', size = ( 1400, 750 ), close_callback=stop)
