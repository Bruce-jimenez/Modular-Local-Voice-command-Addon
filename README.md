# Offline AI Speech Recognition & Voice Command System

## Project Overview

This project is an offline AI speech recognition system designed to convert spoken English into text and identify predefined voice commands.

The long-term goal is to create a modular speech-processing system that can eventually be integrated into other applications, including future robotics projects such as robotic arms, drones, or autonomous systems.

The current version is an early prototype focused on establishing and testing the fundamental speech recognition pipeline. No robotics hardware is currently integrated.

---

# Version 0.01

**Status:** Initial Prototype

The primary goal of Version 0.01 was to successfully capture microphone audio, process it locally, and convert spoken English into text using an offline AI speech recognition model.

The project also includes an initial command detection system that can identify predefined system phrases.

---

# Current Features

- Microphone audio capture
- Offline English speech recognition
- Local Whisper-based transcription
- 16 kHz mono audio processing
- Audio buffering using Python queues
- NumPy audio processing
- Predefined voice command detection
- Modular Python project structure
- Automated command detection testing with Pytest
- No cloud-based speech recognition API required

---

# System Architecture

The current Version 0.01 pipeline is:

```text
              Microphone
                   │
                   ▼
          ┌─────────────────┐
          │  Audio Capture  │
          │   SoundDevice   │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │  Audio Buffer   │
          │ Queue / NumPy   │
          └────────┬────────┘
                   │
                   ▼
          ┌─────────────────┐
          │  faster-whisper │
          │  Speech-to-Text │
          └────────┬────────┘
                   │
                   ▼
             Transcribed Text
                   │
                   ▼
          ┌─────────────────┐
          │ Command Detector│
          └────────┬────────┘
                   │
                   ▼
             System Command
```

---

# Project Structure

```text
Offline_Voice_CMDs/
│
├── src/
│   ├── __init__.py
│   ├── main.py
│   ├── audio.py
│   ├── command_detector.py
│   ├── config.py
│   └── speech_recognizer.py
│
├── test/
│   └── test_command_dectector.py
│
├── LICENSE
├── requirements.txt
├── README.md
└── .gitignore
```

---

# Implementation

## 1. Audio Capture

The `audio.py` module is responsible for receiving audio from the computer's microphone.

The project currently uses SoundDevice for microphone input.

The audio configuration is:

```text
Sample Rate: 16,000 Hz
Channels:    1
Format:      float32
```

The microphone callback receives small audio chunks and places them into a queue.

```python
audio_data = indata[:, 0].copy()
self.audio_queue.put(audio_data)
```

This separates microphone capture from the speech recognition process.

---

## 2. Audio Buffering

Individual microphone chunks are too small to directly use as meaningful speech input.

For the initial transcription test, multiple audio chunks are collected and combined into one larger NumPy array.

```python
audio_data = np.concatenate(audio_chunks)
```

The prototype currently collects approximately **five seconds of audio** before sending it to the speech recognition model.

At a 16 kHz sample rate:

```text
16,000 samples/second
×
5 seconds
=
80,000 samples
```

This provides the Whisper model with enough audio to process a spoken sentence.

---

## 3. Offline Speech Recognition

The `speech_recognizer.py` module uses `faster-whisper` to perform local speech recognition.

The Whisper model is configured to run on the CPU:

```python
WhisperModel(
    MODEL_SIZE,
    device="cpu",
    compute_type="int8"
)
```

The system is configured for English:

```python
LANGUAGE = "en"
```

The captured audio is passed to the recognizer:

```python
text = recognizer.transcribe(audio_data)
```

The resulting text is then displayed in the terminal.

Example:

```text
You said: Hello, this is a test of my offline speech recognition system.
```

This successfully demonstrated the first complete speech-to-text pipeline.

---

# 4. Command Detection

The `command_detector.py` module is responsible for identifying predefined commands from transcribed text.

The current command set includes:

```text
start listening
start recording
start transcription

stop listening
stop recording
stop transcription
```

The detector converts recognized phrases into predefined system commands.

For example:

```text
"start listening"
        ↓
START_LISTENING
```

and:

```text
"stop recording"
        ↓
STOP_RECORDING
```

If the spoken text does not contain a recognized command, the detector returns:

```text
None
```

The command detector is intentionally separated from the speech recognition system so that new commands can be added without modifying the Whisper implementation.

---

# 5. Configuration

The `config.py` module stores settings used by different parts of the application.

Current configuration includes:

```python
MODEL_SIZE = "base"
LANGUAGE = "en"

SAMPLE_RATE = 16000
CHANNELS = 1
```

Keeping configuration values in a separate module makes the project easier to modify and maintain.

---

# Testing

Pytest is currently used to verify the command detection system.

The tests verify that predefined phrases return the correct system commands.

Example:

```text
Input:
"start listening"

Expected:
START_LISTENING
```

Another example:

```text
Input:
"stop recording"

Expected:
STOP_RECORDING
```

Normal speech that does not contain a predefined command should return:

```text
None
```

The initial test suite successfully passed after resolving the project package/import structure.

---

# Development Milestones

## Version 0.01 — Initial Prototype

### Completed

- [x] Created modular Python project structure
- [x] Created `src` package
- [x] Created configuration module
- [x] Implemented microphone audio capture
- [x] Implemented audio buffering
- [x] Configured 16 kHz mono audio
- [x] Installed and configured `faster-whisper`
- [x] Loaded Whisper model locally
- [x] Successfully transcribed English speech
- [x] Created predefined command detector
- [x] Added command detector unit tests
- [x] Verified command detection using Pytest
- [x] Confirmed the basic offline speech-to-text pipeline works

### Current Pipeline

```text
Microphone
    ↓
SoundDevice
    ↓
Audio Chunks
    ↓
Audio Buffer
    ↓
NumPy Array
    ↓
faster-whisper
    ↓
English Text
    ↓
Command Detector
```

---

# Why Offline?

The system is designed to perform speech recognition locally rather than relying on an online speech recognition service.

This provides several potential advantages:

- Reduced dependence on internet connectivity
- Greater control over user audio
- Potentially lower privacy concerns
- Ability to operate in environments without reliable internet
- Easier integration with local hardware systems

The current prototype still downloads the Whisper model from Hugging Face during initial setup. Once the model is available locally, speech transcription itself is performed on the computer.

---

# Future Robotics Implementation

Robotics integration is **not part of Version 0.01**.

However, the project is intentionally structured so that the speech recognition layer can eventually act as a communication interface for other systems.

The future architecture could be:

```text
                 Human Voice
                      │
                      ▼
                 Microphone
                      │
                      ▼
              Audio Processing
                      │
                      ▼
               Speech-to-Text
                      │
                      ▼
              Command Detector
                      │
                      ▼
               State Machine
                      │
                      ▼
              Command Interface
                      │
            ┌─────────┴─────────┐
            ▼                   ▼
       Application        Robotics System
                                │
                    ┌───────────┼───────────┐
                    ▼           ▼           ▼
                  Drone      Robot Arm   Mobile Robot
```

For example, a future system could interpret:

```text
"Move forward"
        ↓
MOVE_FORWARD
```

or:

```text
"Turn left"
        ↓
TURN_LEFT
```

The voice recognition system would not directly control the motors or hardware.

Instead, it would produce a standardized command that another software layer could interpret.

This separation allows the speech recognition system to remain reusable across different future projects.

---

# Planned Improvements

## 1. Continuous Transcription

The current prototype records approximately five seconds of audio before sending it to Whisper.

The next major improvement is continuous speech recognition:

```text
Listen
  ↓
Capture Audio
  ↓
Transcribe
  ↓
Display Text
  ↓
Continue Listening
  ↓
Capture More Audio
  ↓
Transcribe
  ↓
...
```

This will move the project closer to real-time operation.

---

## 2. Voice Activity Detection

The current system uses a fixed recording period.

A future Voice Activity Detection system will determine when the user starts and stops speaking.

```text
Silence
   ↓
Speech Detected
   ↓
Begin Recording
   ↓
User Speaks
   ↓
Speech Ends
   ↓
Transcribe
```

This should reduce unnecessary processing and improve responsiveness.

---

## 3. Command Processing

The command detector will eventually be connected directly to the transcription pipeline.

The intended flow is:

```text
Speech
  ↓
Whisper
  ↓
Text
  ↓
Command Detector
  ↓
System Command
```

For example:

```text
User:
"Start listening"

        ↓

Whisper:

"start listening"

        ↓

Command Detector:

START_LISTENING
```

---

## 4. State Machine

A state machine will eventually control how the application behaves.

Potential states include:

```text
IDLE
LISTENING
RECORDING
TRANSCRIBING
```

For example:

```text
             START_LISTENING
                    │
                    ▼
              ┌───────────┐
              │ LISTENING │
              └─────┬─────┘
                    │
              STOP_LISTENING
                    │
                    ▼
                 ┌──────┐
                 │ IDLE │
                 └──────┘
```

This will allow commands to change the behavior of the application instead of simply being printed to the terminal.

---

## 5. Reduce Latency

Future versions will investigate methods to reduce the delay between speaking and receiving a transcription.

Potential improvements include:

- Smaller Whisper models
- GPU acceleration
- Smaller audio buffers
- Voice Activity Detection
- Asynchronous processing
- Optimized audio handling

The goal is to make the system feel responsive enough for real-time interaction.

---

## 6. Improve Command Reliability

Speech recognition may produce slightly different text from what the user actually says.

Future command detection could account for:

```text
"start listening"
"begin listening"
"activate listening"
```

and potentially map these variations to:

```text
START_LISTENING
```

Additional improvements could include:

- Fuzzy matching
- Command confirmation
- Context-aware commands
- Duplicate command prevention
- Handling transcription errors

---

# Current Challenges

### Transcription Latency

Whisper requires computational resources to process audio. Larger models can provide better recognition but may increase processing time.

### Audio Quality

Background noise, microphone quality, microphone distance, and different recording devices can affect transcription accuracy.

### Real-Time Processing

Continuous transcription introduces additional challenges involving:

- Audio buffering
- Timing
- Threading
- Processing latency
- Speech segmentation

### Command Reliability

The command detector depends on the text produced by the speech recognition model. Incorrect transcription can therefore result in missed or incorrect commands.

### Future Hardware Integration

When robotics are eventually introduced, recognized commands will need to be safely translated into hardware actions.

---

# Technologies

| Technology | Purpose |
|---|---|
| Python | Main programming language |
| faster-whisper | Offline speech recognition |
| SoundDevice | Microphone/audio capture |
| NumPy | Audio buffer processing |
| Pytest | Automated testing |
| Whisper | Speech recognition model architecture |

---

# Project Status

**Version:** 0.01  
**Status:** Initial Prototype / In Development

### Completed

- [x] Project structure
- [x] Microphone capture
- [x] Audio buffering
- [x] Local Whisper model
- [x] English speech-to-text
- [x] Five-second transcription test
- [x] Command detector
- [x] Command detector tests

### Next Version

- [ ] Continuous transcription
- [ ] Integrate command detector with transcription
- [ ] Application state management
- [ ] Real-time command processing

### Future

- [ ] Voice Activity Detection
- [ ] Reduce transcription latency
- [ ] Improve command matching
- [ ] Expand automated testing
- [ ] Performance benchmarking
- [ ] Robotics command interface
- [ ] Integration with future robotic hardware

---

# License

This project is licensed under the terms provided in the `LICENSE` file.
