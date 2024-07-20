from abc import ABC, abstractmethod

from faster_whisper import WhisperModel

from supported_languages import languages
from utils.transcribe_from_audio_frames import transcribe_from_audio_frames


class WordCounter(ABC):
    speech_transcriber: WhisperModel | None = None

    def __init__(
        self, language: str | None = None, words_to_count: list[str] | None = None
    ):
        """
        loads a whisper transcriber model, use `start` function to launch the counter

        ### Parameters
        `words_to_count`: if value is not `None` (default), all words that are not
        included in specified list will be ignored
        """

        if language is not None and language not in languages:
            raise ValueError("selected language is not supported")
        self.language = language

        if words_to_count:
            self.words_to_count = [word.strip().casefold() for word in words_to_count]
        else:
            self.words_to_count = None

        self.words_count_values = {}

        self.full_text = ""

        if not WordCounter.speech_transcriber:
            print("loading a transcribing model")

            WordCounter.speech_transcriber = WhisperModel(
                model_size_or_path="small", device="cpu", compute_type="int8"
            )

    # def _count_stats_from_audio_fragment(self, audio_fragment_frames: list[bytes],
    #                                      sample_rate: int):
    #     print('started transcribing')

    #     spoken_text = transcribe_from_audio_frames(WordCounter.speech_transcriber,
    #                                                audio_fragment_frames,
    #                                                sample_rate, self.language)

    #     self._count_stats(spoken_text)

    def _count_stats(self, spoken_text: str):
        punctuation = r"""!"#$%&'()*+,./:;<=>?@[\]^_`{|}~"""

        self.full_text += " " + spoken_text

        words = (
            spoken_text.translate(str.maketrans("", "", punctuation)).lower().split(" ")
        )

        filtered_words = []
        if self.words_to_count:
            filtered_words = [
                word
                for word in words
                if word.strip() != "" and word in self.words_to_count
            ]
        else:
            filtered_words = [word for word in words if word.strip() != ""]

        for word in filtered_words:
            if word in self.words_count_values:
                self.words_count_values[word] += 1
            else:
                self.words_count_values[word] = 1

    @abstractmethod
    def start(self):
        pass
