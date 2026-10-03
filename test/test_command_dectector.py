# tests/test_command_detector.py

import sys
from pathlib import Path

sys.path.insert(0, str(Path(__file__).resolve().parents[1]))
sys.path.insert(0, str(Path(__file__).resolve().parents[1] / "src"))

try:
    from src.command_detector import detect_system_command  # type: ignore[import-not-found]
except ImportError:
    from command_detector import detect_system_command # type: ignore


def test_start_listening():
    result = detect_system_command("start listening")

    assert result == "START_LISTENING"


def test_start_recording():
    result = detect_system_command("start recording")

    assert result == "START_RECORDING"


def test_start_transcription():
    result = detect_system_command("start transcription")

    assert result == "START_TRANSCRIPTION"


def test_stop_listening():
    result = detect_system_command("stop listening")

    assert result == "STOP_LISTENING"


def test_stop_recording():
    result = detect_system_command("stop recording")

    assert result == "STOP_RECORDING"


def test_stop_transcription():
    result = detect_system_command("stop transcription")

    assert result == "STOP_TRANSCRIPTION"


def test_normal_speech():
    result = detect_system_command(
        "I am testing my offline speech recognition system"
    )

    assert result is None