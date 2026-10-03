# src/config.py

# Whisper model
MODEL_SIZE = "base"

# Speech recognition settings
LANGUAGE = "en"

# Audio settings
SAMPLE_RATE = 16000
CHANNELS = 1

# System commands
SYSTEM_COMMANDS = {
    "start listening": "START_LISTENING",
    "start recording": "START_RECORDING",
    "start transcription": "START_TRANSCRIPTION",

    "stop listening": "STOP_LISTENING",
    "stop recording": "STOP_RECORDING",
    "stop transcription": "STOP_TRANSCRIPTION"
}