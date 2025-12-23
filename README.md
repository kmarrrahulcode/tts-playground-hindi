# TTS Playground

A unified Python framework for Hindi Text-to-Speech synthesis, supporting multiple state-of-the-art TTS models through a consistent API.

## Overview

TTS Playground provides a modular, extensible architecture for experimenting with various Hindi TTS models. Whether you need voice cloning, multi-speaker synthesis, or fast lightweight inference, this framework offers a unified interface to work with different engines seamlessly.

## Supported Models

| Model | Parameters | Voice Cloning | Multi-Speaker | Speed | Best For |
|-------|------------|---------------|---------------|-------|----------|
| **Kokoro** | 82M | ❌ | ✅ (4 voices) | Fast | Lightweight, real-time |
| **XTTS-Hindi** | ~1B | ✅ | ❌ | Slow | Voice cloning |
| **F5-Hindi** | 151M | ✅ | ❌ | Medium | Voice cloning |
| **Indic Parler** | 880M | ❌ | ✅ (22 languages) | Medium | Multilingual Indian languages |
| **VibeVoice Hindi** | 1.5B | ✅ | ✅ (4 speakers) | Medium | High-quality, expressive speech |



## Quick Start

```python
from tts_playground import get_tts_engine

# Initialize Kokoro - fast, lightweight Hindi TTS
tts = get_tts_engine("kokoro", device="cpu")
tts.initialize()

# Generate speech
tts.synthesize(
    text="नमस्ते, यह हिंदी टेक्स्ट टू स्पिच का उदाहरण है।",
    voice="hm_psi",  # Hindi Female
    output_path="output.wav"
)
```

## Installation

### Requirements
- Python 3.10-3.11
- CUDA-capable GPU (recommended for larger models)
- FFmpeg (for audio processing)

### Model-Specific Setup

Each model requires its own virtual environment due to dependency conflicts:

```bash
# VibeVoice Hindi (1.5B - GPU recommended)
python -m venv venv-vibevoice
source venv-vibevoice/bin/activate  # Linux/Mac
pip install -r requirements-vibevoice.txt
pip install -e .

# F5-Hindi
python -m venv venv-f5hindi
source venv-f5hindi/bin/activate
pip install -r requirements-f5hindi.txt
pip install -e .

# Kokoro (lightweight)
python -m venv venv-kokoro
source venv-kokoro/bin/activate
pip install -r requirements-kokoro.txt
pip install -e .

# Indic Parler
python -m venv venv-parler
source venv-parler/bin/activate
pip install -r requirements-parler.txt
pip install -e .
```

## Model Details

### Kokoro TTS

**Model**: [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M)

Lightweight, fast TTS model with multiple Hindi voice presets.

```python
tts = get_tts_engine("kokoro", device="cpu")
tts.initialize()

tts.synthesize(
    text="नमस्ते, आप कैसे हैं?",
    voice="hf_alpha",  # Hindi Female
    speed=1.0,
    output_path="output.wav"
)
```

**Available Voices**: `hf_alpha` (Female), `hf_beta` (Female), `hm_omega` (Male), `hm_psi` (Male)

---

### XTTS-Hindi

**Model**: [Abhinay45/XTTS-Hindi-finetuned](https://huggingface.co/Abhinay45/XTTS-Hindi-finetuned)

Voice cloning model based on Coqui XTTS, fine-tuned for Hindi.

```python
tts = get_tts_engine("xtts-hindi", device="cpu")
tts.initialize()

tts.synthesize(
    text="आपकी आवाज़ में बोल रहा हूं।",
    speaker_wav="my_voice.wav",  # 3-10 second sample
    language="hi",
    output_path="output.wav"
)
```

---

### F5-Hindi

**Model**: [SPRINGLab/F5-Hindi-24KHz](https://huggingface.co/SPRINGLab/F5-Hindi-24KHz)

High-quality voice cloning model optimized for Hindi at 24kHz sample rate.

```python
tts = get_tts_engine("f5-hindi", device="cuda")
tts.initialize()

tts.synthesize(
    text="यह मेरी आवाज़ की क्लोनिंग है।",
    speaker_wav="reference.wav",
    ref_text="Reference audio transcript",  # Optional, improves quality
    output_path="cloned.wav"
)
```

---

### Indic Parler TTS

**Model**: [ai4bharat/indic-parler-tts](https://huggingface.co/ai4bharat/indic-parler-tts)

Multilingual TTS supporting 22 Indian languages with voice description-based synthesis.

```python
tts = get_tts_engine("indic-parler", device="cuda")
tts.initialize()

tts.synthesize(
    text="नमस्ते दोस्तों",
    description="A female speaker with a calm and clear voice.",
    output_path="output.wav"
)
```

**Supported Languages**: Hindi, Tamil, Telugu, Bengali, Marathi, Gujarati, Kannada, Malayalam, Punjabi, Odia, Assamese, English, Nepali, Sanskrit, Sindhi, Kashmiri, Dogri, Maithili, Manipuri, Santali, Bodo, Konkani

---

### VibeVoice Hindi 1.5B

**Model**: [tarun7r/vibevoice-hindi-1.5B](https://huggingface.co/tarun7r/vibevoice-hindi-1.5B)

A frontier TTS model fine-tuned for Hindi, built on Microsoft's VibeVoice architecture. Supports voice cloning, multi-speaker conversations, and long-form audio generation.

```python
tts = get_tts_engine("vibevoice-hindi", device="cuda")
tts.initialize()

# Built-in speakers
tts.synthesize(text="नमस्ते", speaker="hi-Priya_woman", output_path="priya.wav")

# Voice cloning
tts.synthesize(text="नमस्ते", speaker_wav="my_voice.wav", output_path="cloned.wav")

# Multi-speaker conversation
dialogue = [
    {"speaker": "hi-Priya_woman", "text": "नमस्ते, कैसे हो?"},
    {"speaker": "hi-Raj_man", "text": "मैं ठीक हूं, धन्यवाद।"},
]
tts.synthesize_conversation(dialogue=dialogue, output_path="conversation.wav")
```

**Available Speakers**: `hi-Priya_woman`, `hi-Raj_man`, `hi-Ananya_woman`, `hi-Vikram_man`

---

## REST API

A FastAPI-based REST API is included for serving TTS models over HTTP.

### Start Server

```bash
cd api
python start_api.py
```

**Endpoints**:
- `POST /synthesize` - Generate speech from text
- `POST /synthesize-with-voice` - Voice cloning
- `GET /models` - List available models
- `GET /speakers?model=<model>` - Get available speakers/voices
- `GET /health` - Health check

**API Documentation**: http://localhost:8000/docs

### Example Request

```python
import requests

response = requests.post("http://localhost:8000/synthesize", json={
    "text": "नमस्ते दुनिया",
    "model": "vibevoice-hindi",
    "speaker": "hi-Priya_woman"
})
```

---

## Google Colab

For GPU-accelerated inference on Colab (T4 GPU):

```python
# Install
!pip install git+https://github.com/vibevoice-community/VibeVoice.git
!pip install soundfile numpy huggingface_hub accelerate

# Clone and setup
!git clone https://github.com/your-repo/tts-playground.git
%cd tts-playground
!pip install -e .

# Use
from tts_playground import get_tts_engine
tts = get_tts_engine("vibevoice-hindi", device="cuda")
tts.initialize()
tts.synthesize(text="नमस्ते", output_path="test.wav")
```

See `COLAB_VIBEVOICE_SETUP.md` for detailed instructions.

---

## Project Structure

```
tts-playground/
├── tts_playground/
│   ├── __init__.py
│   ├── base.py                 # Base TTS interface
│   ├── factory.py              # Engine factory
│   ├── vibevoice_hindi/        # VibeVoice Hindi implementation
│   ├── f5_hindi/               # F5-Hindi implementation
│   ├── xtts_hindi/             # XTTS-Hindi implementation
│   ├── indic_parler/           # Indic Parler implementation
│   └── kokoro/                 # Kokoro implementation
├── api/
│   ├── main.py                 # FastAPI server
│   └── start_api.py            # Server launcher
├── examples/                   # Usage examples
├── output/                     # Generated audio files
├── requirements-*.txt          # Model-specific dependencies
└── setup_*.py                  # Model-specific setup scripts
```

---

## API Reference

### Factory Function

```python
get_tts_engine(engine_name: str, device: str = "cpu", **kwargs) -> TTSBase
```

**Supported Engines**: `vibevoice-hindi`, `f5-hindi`, `xtts-hindi`, `indic-parler`, `kokoro`

### Common Interface

All engines implement the `TTSBase` interface:

```python
class TTSBase:
    def initialize(self) -> None
    def synthesize(text: str, output_path: str = None, **kwargs) -> str
    def synthesize_batch(texts: List[str], output_dir: str, **kwargs) -> List[str]
    def get_supported_languages(self) -> List[str]
```

---

## Model Comparison

| Feature | VibeVoice | F5-Hindi | XTTS | Indic Parler | Kokoro |
|---------|-----------|----------|------|--------------|--------|
| Voice Cloning | ✅ | ✅ | ✅ | ❌ | ❌ |
| Multi-Speaker | ✅ | ❌ | ❌ | ✅ | ✅ |
| Languages | Hindi | Hindi | Hindi | 22 Indian | Hindi |
| GPU Required | Recommended | Recommended | Optional | Recommended | No |
| Sample Rate | 24kHz | 24kHz | 24kHz | 22kHz | 24kHz |
| Inference Speed | Medium | Medium | Slow | Medium | Fast |

---

## Troubleshooting

### FFmpeg Not Found
Install FFmpeg and add to PATH:
- **Windows**: Download from [gyan.dev](https://www.gyan.dev/ffmpeg/builds/) (full-shared version)
- **Linux**: `apt install ffmpeg`
- **Mac**: `brew install ffmpeg`

### CUDA Out of Memory
- Use `device="cpu"` for smaller models
- Reduce batch size
- Use float16: Models load with `torch.float16` by default on CUDA

### Dependency Conflicts
Each model has specific dependency requirements. Always use the corresponding virtual environment.

---

## License

This repository's **code** is licensed under the MIT License.

**Important**: The TTS models used in this project have their own licenses. Please review each model's license before use:

| Model | License | Links |
|-------|---------|-------|
| VibeVoice Hindi 1.5B | MIT | [HuggingFace](https://huggingface.co/tarun7r/vibevoice-hindi-1.5B) · [GitHub](https://github.com/vibevoice-community/VibeVoice) |
| F5-Hindi | CC-BY-NC-4.0 | [HuggingFace](https://huggingface.co/SPRINGLab/F5-Hindi-24KHz) |
| XTTS-Hindi | CPML | [HuggingFace](https://huggingface.co/Abhinay45/XTTS-Hindi-finetuned) · [Coqui TTS](https://github.com/coqui-ai/TTS) |
| Indic Parler TTS | Apache 2.0 | [HuggingFace](https://huggingface.co/ai4bharat/indic-parler-tts) |
| Kokoro | Apache 2.0 | [HuggingFace](https://huggingface.co/hexgrad/Kokoro-82M) |

Please ensure compliance with each model's license terms for your use case.

---

## Contributing

Contributions are welcome. Please submit a pull request or open an issue for discussion.

## Acknowledgments

- [VibeVoice Community](https://github.com/vibevoice-community/VibeVoice)
- [SPRINGLab](https://huggingface.co/SPRINGLab)
- [AI4Bharat](https://ai4bharat.org/)
- [Coqui TTS](https://github.com/coqui-ai/TTS)
- [Hexgrad](https://huggingface.co/hexgrad)
