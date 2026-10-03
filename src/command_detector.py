# src/command_detector.py

from config import SYSTEM_COMMANDS


def detect_system_command(text):
    text = text.lower().strip()

    for phrase, command in SYSTEM_COMMANDS.items():
        if phrase in text:
            return command

    return None