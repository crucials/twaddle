import time
import faulthandler
from typing import Optional

import pyaudio

from ui.errors.transcriber_not_initialized_error import TranscriberNotInitializedError
from word_counters import WordCounter
from utils.transcribe_from_audio_frames import transcribe_from_audio_frames


class RealtimeWordCounter(WordCounter):
    def __init__(
        self,
        language: str | None = None,
        recording_device_index: int | None = None,
        words_to_count: list[str] | None = None,
    ):
        super().__init__(language, words_to_count)

        self.recording_device_index = recording_device_index

        self.running = False
        self.__finished_last_transcribing = True

    def _count_stats_from_audio_fragment(
        self, audio_fragment_frames: list[bytes], sample_rate: int
    ):
        if not self.running:
            self.__finished_last_transcribing = False

        if WordCounter.speech_transcriber is None:
            raise TranscriberNotInitializedError()

        print("started transcribing")

        spoken_text = transcribe_from_audio_frames(
            WordCounter.speech_transcriber,
            audio_fragment_frames,
            sample_rate,
            self.language,
        )

        print("finished transcription")

        self._count_stats(spoken_text)

        if not self.running:
            self.__finished_last_transcribing = True

    def start(self):
        """
        starts recording mic input, transcribes and counts words. blocks
        the current thread execution until the counter is stopped
        """
        READ_CHUNK = 1024
        SAMPLE_RATE = 44100
        AUDIO_FRAGMENT_SECONDS = 10

        audio = None
        microphone_stream = None
        try:
            faulthandler.enable()
            audio = pyaudio.PyAudio()
            microphone_stream = audio.open(
                rate=SAMPLE_RATE,
                channels=2,
                format=pyaudio.paInt16,
                input=True,
                input_device_index=self.recording_device_index,
                output=True,
            )
            print(f"recording from mic ({self.recording_device_index}) started")

            self.running = True
            while self.running:
                print("recording fragment")
                microphone_audio_frames = []

                for _ in range(
                    0, int(SAMPLE_RATE / READ_CHUNK * AUDIO_FRAGMENT_SECONDS)
                ):
                    if not self.running:
                        break
                    microphone_audio_frames.append(
                        microphone_stream.read(READ_CHUNK, exception_on_overflow=False)
                    )

                if not self.running:
                    break

                self._count_stats_from_audio_fragment(
                    microphone_audio_frames, SAMPLE_RATE
                )
        finally:
            print("closing mic stream")
            if microphone_stream:
                microphone_stream.stop_stream()
                microphone_stream.close()

            if audio:
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
            if (
                self.__finished_last_transcribing
                or seconds_waited == seconds_timeout
                or seconds_timeout is None
            ):
                break
            time.sleep(1)
            seconds_waited += 1
