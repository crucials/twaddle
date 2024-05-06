import wave
import os
import time
from datetime import datetime
from typing import Optional
import faulthandler

import pyaudio
from faster_whisper import WhisperModel

from supported_languages import languages
from utils.transcribe_from_bytes import transcribe_from_bytes


speech_transcriber: WhisperModel | None = None

class WordCounter:
    def __init__(self, language: str = 'en',
                 recording_device_index: int | None = None,
                 words_to_count: list[str] | None = None):
        """
        loads a whisper transcriber model, use `start` function to launch the counter
        
        ### Parameters
        `words_to_count`: if value is not `None` (default), all words that are not
        included in specified list will be ignored
        """
        global speech_transcriber
        
        if language not in languages:
            raise ValueError('selected language is not supported')
        self.language = language

        self.recording_device_index = recording_device_index

        self.running = False
        self.__finished_last_transcribing = True

        if words_to_count:
            self.words_to_count = [word.strip().casefold() for word in words_to_count]
        else:
            self.words_to_count = None

        self.words_count_values = {}

        self.full_text = ''

        if not speech_transcriber:
            print('loading a transcribing model')

            speech_transcriber = WhisperModel(model_size_or_path='small',
                                              device='cpu',
                                              compute_type='int8')

    def __count_stats_for_audio_fragment(self, audio_fragment_frames: list[bytes],
                                         sample_rate: int):
            global speech_transcriber
            punctuation = r"""!"#$%&'()*+,./:;<=>?@[\]^_`{|}~"""

            if not self.running:
                self.__finished_last_transcribing = False

            print('started transcribing')

            spoken_text = transcribe_from_bytes(speech_transcriber, audio_fragment_frames,
                                                sample_rate, self.language)

            self.full_text += ' ' + spoken_text

            words = (
                spoken_text
                .translate(str.maketrans('', '', punctuation))
                .lower()
                .split(' ')
            )
            
            filtered_words = []
            if self.words_to_count:
                filtered_words = [word for word in words
                                  if word.strip() != ''
                                  and word in self.words_to_count]
            else:
                filtered_words = [word for word in words if word.strip() != '']
            
            for word in filtered_words:
                if word in self.words_count_values:
                    self.words_count_values[word] += 1
                else:
                    self.words_count_values[word] = 1

            if not self.running:
                self.__finished_last_transcribing = True

            return spoken_text

    def start(self):
        """
        starts recording mic input, transcribes and counts words. blocks 
        the current thread execution until the counter is stopped
        """
        global speech_transcriber

        READ_CHUNK = 1024
        SAMPLE_RATE = 44100
        AUDIO_FRAGMENT_SECONDS = 10

        audio = None
        microphone_stream = None
        try:
            faulthandler.enable()
            audio = pyaudio.PyAudio()
            microphone_stream = audio.open(rate=SAMPLE_RATE,
                                           channels=2,
                                           format=pyaudio.paInt16,
                                           input=True,
                                           input_device_index=self.recording_device_index,
                                           output=True)
            print(f'recording from mic ({self.recording_device_index}) started')

            self.running = True
            while self.running:
                print('recording fragment')
                microphone_audio_frames = []

                for chunk_number in range(0, int(SAMPLE_RATE / READ_CHUNK * AUDIO_FRAGMENT_SECONDS)):
                    if not self.running:
                        break
                    microphone_audio_frames.append(
                        microphone_stream.read(READ_CHUNK, exception_on_overflow=False)
                    )

                if not self.running:
                    break
                    
                self.__count_stats_for_audio_fragment(microphone_audio_frames,
                                                      SAMPLE_RATE)
        finally:
            print('closing mic stream')
            if microphone_stream:
                microphone_stream.stop_stream()
                microphone_stream.close()

            if audio:
                print('terminate')
                audio.terminate()

    def stop(self, seconds_timeout: Optional[int] = 5):
        """
        stops the counter and blocks the current execution until counter finishes
        transcribing with a 5 second timeout

        ### Parameters

        `seconds_timeout`: seconds to wait until transcription is finished,
        if set to `None`, function doesnt wait
        """

        self.running = False

        # wait until counter finishes transcribing with a 5 second timeout
        seconds_waited = 0
        while True:
            if self.__finished_last_transcribing or seconds_waited == seconds_timeout or seconds_timeout == None:
                break
            time.sleep(1)
            seconds_waited += 1
