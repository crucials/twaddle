import os

import eel

from utils.create_path_from_executable import create_path_from_executable
from ui.count_from_microphone import start_counter_from_microphone, reset_counter


eel.browsers.set_path('chrome', create_path_from_executable('..', 'bin', 'ungoogled-chromium_120.0.6099.109-1.1.AppImage'))

eel.init('src/ui/web/dist')
eel.start('index.html', mode = 'chrome', size = ( 1400, 750 ))
