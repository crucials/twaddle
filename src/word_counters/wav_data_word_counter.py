import time
import faulthandler
from typing import Optional

import pyaudio
from faster_whisper import WhisperModel

from word_counters import WordCounter


class WavDataWordCounter(WordCounter):
    def __init__(self,
                 wav_data: bytes,
                 language: str | None = None,
                 words_to_count: list[str] | None = None):
        super().__init__(language, words_to_count)
