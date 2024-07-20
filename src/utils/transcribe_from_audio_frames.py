import wave
from datetime import datetime
import os

from faster_whisper import WhisperModel
import pyaudio


def transcribe_from_audio_frames(
    transcription_model: WhisperModel,
    audio_data: list[bytes],
    audio_sample_rate: int,
    language: str | None,
):
    """
    writes specified audio data to a file with unix timestamp as its name
    (like this: `1714995779.mp3`), then passes this filename to whisper model

    deletes created file on exit
    """

    audio_file_path = "./" + str(datetime.now().timestamp()) + ".wav"
    with wave.open(audio_file_path, "wb") as fragment_file_stream:
        fragment_file_stream.setnchannels(2)
        fragment_file_stream.setsampwidth(pyaudio.get_sample_size(pyaudio.paInt16))
        fragment_file_stream.setframerate(audio_sample_rate)
        fragment_file_stream.writeframes(b"".join(audio_data))

    try:
        segments_iterator, _ = transcription_model.transcribe(
            audio_file_path, language=language, condition_on_previous_text=True
        )

        return " ".join([segment.text for segment in segments_iterator])
    except Exception as error:
        raise error
    finally:
        os.remove(audio_file_path)
