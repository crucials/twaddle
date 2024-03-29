import wave
import string
from datetime import datetime
import os
from threading import Thread
from types import SimpleNamespace
from typing import Literal

import pyaudio
import whisper


Language = Literal['ru', 'en']

counter_running = False
words_count_values = {}

def __transcribe(speech_transcriber: whisper.Whisper, audio_file_path: str,
                 language: Language):
    global words_count_values

    print('started transcribing')
    response = speech_transcriber.transcribe(audio_file_path, language=language,
                                             condition_on_previous_text=True)
    os.remove(audio_file_path)

    spoken_text = (
        response['text'].translate(str.maketrans('', '', string.punctuation))
        .lower()
    )
    
    for spoken_word in filter(lambda word: word.strip() != '', spoken_text.split(' ')):
        if spoken_word in words_count_values:
            words_count_values[spoken_word] += 1
        else:
            words_count_values[spoken_word] = 1

    return response

def start_counting(language: Language):
    global counter_running
    global words_count_values

    print('loading a transcribe model')
    speech_transcriber = whisper.load_model('small')

    READ_CHUNK = 1024
    SAMPLE_RATE = 44100
    AUDIO_FRAGMENT_SECONDS = 10

    audio = pyaudio.PyAudio()

    microphone_stream = None
    try:
        microphone_stream = audio.open(rate=SAMPLE_RATE, channels=2,
                                        format=pyaudio.paInt16, input=True, output=True)
        print('recording from mic started')

        counter_running = True
        while counter_running:
            print('recording fragment')
            microphone_audio_frames = []
            for chunk_number in range(0, int(SAMPLE_RATE / READ_CHUNK * AUDIO_FRAGMENT_SECONDS)):
                if not counter_running:
                    break
                microphone_audio_frames.append(microphone_stream.read(READ_CHUNK))
            
            audio_fragment_path = './' + str(datetime.now().timestamp()) + '.wav'
            with wave.open(audio_fragment_path, 'wb') as fragment_file_stream:
                fragment_file_stream.setnchannels(2)
                fragment_file_stream.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
                fragment_file_stream.setframerate(SAMPLE_RATE)
                fragment_file_stream.writeframes(b''.join(microphone_audio_frames))
                
            # thread = Thread(target=lambda: __transcribe(speech_transcriber,
            #                                           audio_fragment_path))
            # thread.start()
            # thread.join()
            __transcribe(speech_transcriber, audio_fragment_path, language)
    finally:
        if microphone_stream:
            microphone_stream.stop_stream()
            microphone_stream.close()

        audio.terminate()

    return words_count_values

def stop_counting():
    global counter_running
    counter_running = False
