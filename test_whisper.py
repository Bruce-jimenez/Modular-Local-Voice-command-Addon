import numpy as np

from src.audio import AudioRecorder
from src.speech_recognizer import SpeechRecognizer
from src.config import SAMPLE_RATE


def main():
    recorder = AudioRecorder()
    recognizer = SpeechRecognizer()

    print("Loading Whisper model...")
    print("Model loaded.")

    recorder.start()

    print("Speak for about 5 seconds...")
    print("Say something like: 'Hello, this is a test of my offline speech recognition system.'")

    try:
        audio_chunks = []

        # Collect approximately 3 seconds of audio
        target_samples = SAMPLE_RATE * 5
        collected_samples = 0

        while collected_samples < target_samples:
            audio = recorder.read()

            audio_chunks.append(audio)
            collected_samples += len(audio)

        # Combine all chunks into one audio array
        audio_data = np.concatenate(audio_chunks)

        print("Processing speech...")

        text = recognizer.transcribe(audio_data)

        print(f"You said: {text}")

    except KeyboardInterrupt:
        print("\nStopping...")

    finally:
        recorder.stop()


if __name__ == "__main__":
    main()