# src/audio.py

import queue
import sounddevice as sd
# import numpy as np

from src.config import SAMPLE_RATE, CHANNELS


class AudioRecorder:
    def __init__(self):
        self.audio_queue = queue.Queue()
        self.stream = None

    def audio_callback(self, indata, frames, time, status):
        if status:
            print(f"Audio status: {status}")

        audio_data = indata[:, 0].copy()
        self.audio_queue.put(audio_data)

    def start(self):
        self.stream = sd.InputStream(
            samplerate=SAMPLE_RATE,
            channels=CHANNELS,
            dtype="float32",
            callback=self.audio_callback
        )

        self.stream.start()

    def read(self):
        return self.audio_queue.get()

    def stop(self):
        if self.stream is not None:
            self.stream.stop()
            self.stream.close()
            self.stream = None