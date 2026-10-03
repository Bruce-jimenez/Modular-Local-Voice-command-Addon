# src/speech_recognizer.py

from faster_whisper import WhisperModel

from config import MODEL_SIZE, LANGUAGE


class SpeechRecognizer:
    def __init__(self):
        self.model = WhisperModel(
            MODEL_SIZE,
            device="cpu",
            compute_type="int8"
        )

    def transcribe(self, audio):
        segments, info = self.model.transcribe(
            audio,
            language=LANGUAGE
        )

        text = ""

        for segment in segments:
            text += segment.text

        return text.strip()