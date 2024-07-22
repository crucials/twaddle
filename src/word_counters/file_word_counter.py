from typing import Optional

from ui.errors.transcriber_not_initialized_error import TranscriberNotInitializedError
from word_counters import WordCounter


class FileWordCounter(WordCounter):
    def __init__(
        self,
        audio_file_path: str,
        language: str | None = None,
        words_to_count: list[str] | None = None,
    ):
        super().__init__(language, words_to_count)

        self.audio_file_path = audio_file_path
        self.audio_file_seconds_duration: Optional[int] = None

    def start(self):
        print("started transcribing")

        if WordCounter.speech_transcriber is None:
            raise TranscriberNotInitializedError()

        segments_iterator, info = WordCounter.speech_transcriber.transcribe(
            self.audio_file_path,
            language=self.language,
            condition_on_previous_text=True,
        )

        self._count_stats(" ".join([segment.text for segment in segments_iterator]))
        self.audio_file_seconds_duration = round(info.duration)

        print("finished transcription")
