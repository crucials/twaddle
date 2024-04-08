import wave
import string
import os
import time
from datetime import datetime
from types import SimpleNamespace
from typing import Literal, Optional

import pyaudio
import whisper

from supported_languages import languages


speech_transcriber: whisper.Whisper | None = None

class WordCounter:
    language = 'en'

    running = False
    __finished_last_transcribing = True
    
    error: Exception | None = None

    words_count_values = {}

    def __init__(self, language: str = 'en'):
        global speech_transcriber

        if language not in languages:
            raise ValueError('selected language is not supported')
        self.language = language

        if not speech_transcriber:
            print('loading a transcribing model')
            speech_transcriber = whisper.load_model('small')

    def __transcribe(self, audio_file_path: str):
            global speech_transcriber

            if not self.running:
                self.__finished_last_transcribing = False

            print('started transcribing')

            response = speech_transcriber.transcribe(audio_file_path, language=self.language,
                                                     condition_on_previous_text=True)
            spoken_text = (
                response['text'].translate(str.maketrans('', '', string.punctuation))
                .lower()
            )
            os.remove(audio_file_path)
            
            for spoken_word in filter(lambda word: word.strip() != '', spoken_text.split(' ')):
                if spoken_word in self.words_count_values:
                    self.words_count_values[spoken_word] += 1
                else:
                    self.words_count_values[spoken_word] = 1

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

        audio = pyaudio.PyAudio()

        microphone_stream = None
        try:
            microphone_stream = audio.open(rate=SAMPLE_RATE, channels=2,
                                            format=pyaudio.paInt16, input=True, output=True)
            print('recording from mic started')

            self.running = True
            while self.running:
                print('recording fragment')
                microphone_audio_frames = []

                for chunk_number in range(0, int(SAMPLE_RATE / READ_CHUNK * AUDIO_FRAGMENT_SECONDS)):
                    if not self.running:
                        break
                    microphone_audio_frames.append(microphone_stream.read(READ_CHUNK))

                if not self.running:
                    break
                
                audio_fragment_path = './' + str(datetime.now().timestamp()) + '.wav'
                with wave.open(audio_fragment_path, 'wb') as fragment_file_stream:
                    fragment_file_stream.setnchannels(2)
                    fragment_file_stream.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
                    fragment_file_stream.setframerate(SAMPLE_RATE)
                    fragment_file_stream.writeframes(b''.join(microphone_audio_frames))
                    
                self.__transcribe(audio_fragment_path)
        finally:
            if microphone_stream:
                microphone_stream.stop_stream()
                microphone_stream.close()

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
