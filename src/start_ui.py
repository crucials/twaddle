from concurrent.futures import ThreadPoolExecutor
import time
import os

import eel

from word_counter import start_counting, stop_counting
from executable_path import executable_path
from ui.start_counter_from_microphone import start_counter_from_microphone


# def start_counting_words():
#     tracked_words = [
#         'test',
#         'word',
#         'another',
#         'might',
#         'work',
#         'speech recognition'
#     ]

#     with ThreadPoolExecutor() as word_counter_executor:
#         word_counting_future = word_counter_executor.submit(start_counting, 'en')
#         time.sleep(10)
#         stop_counting()
#         word_counts = word_counting_future.result() 
#         print('\n'.join([f'{word}: {word_counts.get(word)}' for word in tracked_words
#                         if word in word_counts]))

eel.browsers.set_path('chrome', os.path.abspath(os.path.join(executable_path, '..', 'bin', 'ungoogled-chromium_120.0.6099.109-1.1.AppImage')))

eel.init('src/ui/web/dist')
eel.start('index.html', mode = 'chrome', size = ( 1400, 750 ))
