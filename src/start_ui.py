import sys

import eel

from utils.create_path_from_executable import create_path_from_executable
from ui.count_from_microphone import start_counter_from_microphone, reset_counter
from ui.get_supported_languages import get_supported_languages


def stop(route, websockets):
    print('exiting')
    reset_counter()

    sys.exit(0)

print('launching')

eel.browsers.set_path('chrome', create_path_from_executable('ui', 'bin', 'ungoogled-chromium_120.0.6099.109-1.1.AppImage'))

eel.init('src/ui/web/dist')
eel.start('index.html', mode = 'chrome', size = ( 1400, 750 ), close_callback=stop)
