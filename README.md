# TTS Playground

A reusable Python module for Text-to-Speech with support for multiple TTS engines, optimized for Hindi language and CPU usage.

## Features

- 🎯 **Modular Design**: Each TTS library is in a separate folder
- 🔌 **Easy Integration**: Simple, unified interface for all TTS engines
- 🇮🇳 **Hindi Support**: Optimized for Hindi text-to-speech
- 💻 **CPU Optimized**: Designed to run efficiently on CPU
- 🔄 **Reusable**: Can be easily integrated into other projects
- 📁 **Organized Output**: Automatically saves files to `output/xtts_hindi/`, `output/indri/`, or `output/kokoro/`

## Quick Start

```python
from tts_playground import get_tts_engine

# Create TTS engine
tts = get_tts_engine("xtts-hindi", device="cpu")  # or "indri", "kokoro"
tts.initialize()

# Synthesize speech (saves to output/xtts_hindi/ by default)
tts.synthesize(
    text="नमस्ते, यह एक टेक्स्ट टू स्पीच उदाहरण है।",
    output_path="hello.wav",
    language="hi"
)
```

---

## Table of Contents

1. [Installation](#installation)
2. [Supported Models](#supported-models)
3. [Usage Examples](#usage-examples)
4. [REST API](#rest-api)
5. [Environment Setup](#environment-setup)
6. [Troubleshooting](#troubleshooting)
7. [API Reference](#api-reference)

---

## Installation

### Python Version Requirement

**⚠️ Important**: The TTS library requires **Python 3.9-3.11** (does not support Python 3.12+).

### Option 1: XTTS-Hindi (Voice Cloning)

```powershell
# Create virtual environment with Python 3.11
py -3.11 -m venv venv

# Activate
.\venv\Scripts\Activate.ps1

# Install
pip install -r requirements.txt
pip install -e .

# Set HuggingFace token
$env:HF_TOKEN="your_token_here"
```

### Option 2: Indri TTS (Pre-trained Speakers)

**Note**: Requires separate environment due to transformers version conflict.

```powershell
# Create separate environment
py -3.11 -m venv venv-indri

# Activate
.\venv-indri\Scripts\Activate.ps1

# Install
pip install -r requirements-indri.txt
pip install -e .

# Set token
$env:HF_TOKEN="your_token_here"
```

### Option 3: Kokoro TTS (Fast, Lightweight)

**Note**: Requires Python 3.10-3.12 (not compatible with Python 3.13+).

```powershell
# Create separate environment with Python 3.11
py -3.11 -m venv venv-kokoro

# Activate
.\venv-kokoro\Scripts\Activate.ps1

# Install
pip install -r requirements-kokoro.txt
pip install -e .
```

---

## Supported Models

### XTTS-Hindi

| Feature | Details |
|---------|---------|
| **Model** | [Abhinay45/XTTS-Hindi-finetuned](https://huggingface.co/Abhinay45/XTTS-Hindi-finetuned) |
| **Language** | Hindi |
| **Voice Cloning** | ✅ Yes (3-10 second audio samples) |
| **Pre-trained Speakers** | ❌ No |
| **Speed** | Slower (higher quality) |
| **Environment** | `venv` |
| **Output Folder** | `output/xtts_hindi/` |

### Indri TTS

| Feature | Details |
|---------|---------|
| **Model** | [11mlabs/indri-0.1-350m-tts](https://huggingface.co/11mlabs/indri-0.1-350m-tts) |
| **Languages** | English, Hindi, Code-mixing |
| **Voice Cloning** | ❌ No |
| **Pre-trained Speakers** | ✅ Yes (13 speakers) |
| **Speed** | Faster (lightweight 350M model) |
| **Environment** | `venv-indri` |
| **Output Folder** | `output/indri/` |

**Indri Speakers**: `[spkr_63]` 🇬🇧 👨, `[spkr_67]` 🇺🇸 👨, `[spkr_68]` 🇮🇳 👨 (default), `[spkr_70]` 🇮🇳 👨, `[spkr_53]` 🇮🇳 👩, and 8 more.

### Kokoro TTS

| Feature | Details |
|---------|---------|
| **Model** | [hexgrad/Kokoro-82M](https://huggingface.co/hexgrad/Kokoro-82M) |
| **Languages** | Hindi (and others) |
| **Voice Cloning** | ❌ No |
| **Pre-trained Speakers** | ✅ Yes (4 Hindi voices) |
| **Speed** | Very Fast (82M lightweight model) |
| **Environment** | `venv-kokoro` |
| **Output Folder** | `output/kokoro/` |
| **Python** | 3.10-3.12 only |

**Kokoro Hindi Voices**: `hf_alpha` 👩 (default), `hf_beta` 👩, `hm_omega` 👨, `hm_psi` 👨

---

## Usage Examples

### XTTS-Hindi: Voice Cloning

```python
from tts_playground import get_tts_engine

tts = get_tts_engine("xtts-hindi", device="cpu")
tts.initialize()

# Clone your voice
tts.synthesize(
    text="यह आपकी आवाज़ में बोल रहा है।",
    output_path="cloned_voice.wav",  # Saves to output/xtts_hindi/cloned_voice.wav
    speaker_wav="my_voice.wav",  # Your 3-10 second voice sample
    language="hi"
)
```

### Indri: Pre-trained Speakers

```python
from tts_playground import get_tts_engine

tts = get_tts_engine("indri", device="cpu")
tts.initialize()

# Use pre-trained speaker
tts.synthesize(
    text="नमस्ते दोस्तों",
    output_path="hindi_speech.wav",  # Saves to output/indri/hindi_speech.wav
    speaker="[spkr_68]",  # Hindi book reader
    max_new_tokens=4096  # For longer text
)

# Code-mixing (English + Hindi)
tts.synthesize(
    text="Hello दोस्तों, welcome to the future",
    output_path="mixed.wav",
    speaker="[spkr_67]"  # US English speaker
)
```

### Batch Processing

```python
texts = ["पहला वाक्य।", "दूसरा वाक्य।", "तीसरा वाक्य।"]

output_paths = tts.synthesize_batch(
    texts=texts,
    output_dir="batch_output",  # Saves to output/indri/batch_output/
)
```

### Kokoro: Fast Hindi TTS

```python
from tts_playground import get_tts_engine

# Available voices: hf_alpha, hf_beta (female), hm_omega, hm_psi (male)
tts = get_tts_engine("kokoro", device="cpu", voice="hf_alpha")

# Synthesize Hindi text
tts.synthesize(
    text="नमस्ते, आप कैसे हैं?",
    output_path="kokoro_hindi.wav",  # Saves to output/kokoro/kokoro_hindi.wav
    speed=1.0  # Adjust speed (0.5-2.0)
)

# Try different voice
tts.synthesize(
    text="यह पुरुष आवाज़ है।",
    output_path="male_voice.wav",
    voice="hm_omega"  # Male voice
)
```

### Disable Default Output Folder

```python
# Save to custom location without output/ prefix
tts.synthesize(
    text="Custom location",
    output_path="my_custom_folder/audio.wav",
    use_default_output_dir=False  # Disables output/indri/ prefix
)
```

---

## REST API

### Start the API Server

```powershell
# Activate environment
.\venv-indri\Scripts\Activate.ps1

# Install API dependencies
pip install -r api/requirements.txt

# Set token
$env:HF_TOKEN="your_token_here"

# Start server
cd api
python start_api.py
```

**API will be available at:**
- API: http://localhost:8000
- Interactive Docs: http://localhost:8000/docs
- Web Client: Open `api/example_client.html` in browser

### Quick API Examples

**Python:**
```python
import requests

# Synthesize with Indri
response = requests.post("http://localhost:8000/synthesize", json={
    "text": "नमस्ते दोस्तों",
    "model": "indri",
    "speaker": "[spkr_68]"
})
print(response.json())
```

**cURL:**
```bash
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text": "नमस्ते", "model": "indri", "speaker": "[spkr_68]"}'
```

**See `api/README_API.md` for complete API documentation.**

---

## Environment Setup

### Switching Between Models

```powershell
# Use XTTS-Hindi
.\venv\Scripts\Activate.ps1
$env:HF_TOKEN="your_token_here"
python examples/example_xtts_hindi.py

# Use Indri
deactivate
.\venv-indri\Scripts\Activate.ps1
$env:HF_TOKEN="your_token_here"
python examples/example_indri.py

# Use Kokoro
deactivate
.\venv-kokoro\Scripts\Activate.ps1
python examples/example_kokoro_hindi.py
```

### Check Active Environment

```powershell
python -c "import sys; print(sys.prefix)"
python -c "import transformers; print(transformers.__version__)"
```

### Virtual Environment Setup (Python 3.12+ Users)

If you have Python 3.12 or 3.13:

1. **Install Python 3.11** from [python.org](https://www.python.org/downloads/)
2. **Create venv with specific Python version**:
   ```powershell
   # Find Python 3.11
   py -3.11 --version
   
   # Create venv
   py -3.11 -m venv venv
   
   # Activate
   .\venv\Scripts\Activate.ps1
   ```

---

## Troubleshooting

### FFmpeg Error (Windows)

**Error**: `Could not load libtorchcodec. Likely causes: FFmpeg is not properly installed`

**Solution**:
1. Download **ffmpeg-release-full-shared.7z** from https://www.gyan.dev/ffmpeg/builds/
2. Extract and add `bin` folder to PATH
3. Verify: `ffmpeg -version`

**Important**: Must use "full-shared" version (not static) for DLL files.

### Transformers Version Conflict

**Error**: `BeamSearchScorer` import errors

**Solution**: Ensure correct environment:
- XTTS: `transformers < 4.40.0` (use `venv`)
- Indri: `transformers >= 4.46.0` (use `venv-indri`)

### Audio Truncation (Indri)

**Problem**: Audio cuts off before text completes

**Solution**: Increase `max_new_tokens`:

```python
tts.synthesize(
    text="Long text here...",
    output_path="output.wav",
    max_new_tokens=8192  # Default: 8192
)
```

| Text Length | Recommended max_new_tokens |
|------------|---------------------------|
| < 50 chars | 2048 (default) |
| 50-150 chars | 4096 |
| 150-300 chars | 8192 |
| 300+ chars | 16384 |

### Common Warnings (Indri)

These warnings are **normal** and can be ignored:
- "attention mask and pad token id were not set"
- "Setting pad_token_id to eos_token_id"
- "To copy construct from a tensor..."

To suppress:
```python
import warnings
warnings.filterwarnings('ignore')
```

---

## API Reference

### Factory Function

```python
get_tts_engine(engine_name: str, **kwargs) -> TTSBase
```

Creates a TTS engine instance.

**Parameters:**
- `engine_name`: `"xtts-hindi"`, `"indri"`, or `"kokoro"`
- `device`: `"cpu"` or `"cuda"` (default: `"cpu"`)
- `hf_token`: HuggingFace token (optional, reads from `HF_TOKEN` env var)

### TTSBase Interface

All engines implement:

```python
class TTSBase:
    def initialize(self) -> None
    def synthesize(text, output_path=None, **kwargs) -> Union[bytes, str]
    def synthesize_batch(texts, output_dir, **kwargs) -> List[str]
    def get_supported_languages(self) -> list
    def is_initialized(self) -> bool
```

### XTTS-Hindi Specific

```python
tts.synthesize(
    text: str,
    output_path: Optional[str] = None,
    speaker_wav: Optional[str] = None,  # Required for voice cloning
    language: str = "hi",
    use_default_output_dir: bool = True,  # Saves to output/xtts_hindi/
)
```

### Indri Specific

```python
tts.synthesize(
    text: str,
    output_path: Optional[str] = None,
    speaker: Optional[str] = None,  # e.g., "[spkr_68]"
    max_new_tokens: int = 8192,  # Increase for longer text
    temperature: float = 1.0,
    use_default_output_dir: bool = True,  # Saves to output/indri/
)

# Get available speakers
speakers = tts.get_available_speakers()
# Returns: {"[spkr_68]": "🇮🇳 👨 book reader", ...}
```

### Kokoro Specific

```python
tts.synthesize(
    text: str,
    output_path: Optional[str] = None,
    voice: Optional[str] = None,  # e.g., "hf_alpha", "hm_omega"
    speed: float = 1.0,  # Speech speed (0.5-2.0)
    use_default_output_dir: bool = True,  # Saves to output/kokoro/
)

# Get available Hindi voices
voices = tts.get_available_voices()
# Returns: {"hf_alpha": "Hindi Female Alpha", "hf_beta": "Hindi Female Beta", 
#           "hm_omega": "Hindi Male Omega", "hm_psi": "Hindi Male Psi"}
```

---

## Project Structure

```
TTS-Playground/
├── output/                    # Generated audio files (auto-created)
│   ├── xtts_hindi/           # XTTS-Hindi outputs
│   ├── indri/                # Indri outputs
│   └── kokoro/               # Kokoro outputs
├── tts_playground/           # Main module
│   ├── __init__.py
│   ├── base.py               # Base TTS interface
│   ├── factory.py            # Factory for creating engines
│   ├── xtts_hindi/           # XTTS-Hindi implementation
│   ├── indri/                # Indri implementation
│   └── kokoro/               # Kokoro implementation
├── examples/                 # Example scripts
│   ├── example_xtts_hindi.py
│   ├── example_indri.py
│   ├── example_kokoro_hindi.py
│   └── voice_cloning_example.py
├── venv/                     # XTTS environment
├── venv-indri/               # Indri environment
├── venv-kokoro/              # Kokoro environment
├── requirements.txt          # XTTS dependencies
├── requirements-indri.txt    # Indri dependencies
├── requirements-kokoro.txt   # Kokoro dependencies
└── README.md                 # This file
```

---

## Examples

Run the example scripts:

```powershell
# XTTS-Hindi examples
.\venv\Scripts\Activate.ps1
python examples/example_xtts_hindi.py

# Indri examples
.\venv-indri\Scripts\Activate.ps1
python examples/example_indri.py

# Kokoro examples
.\venv-kokoro\Scripts\Activate.ps1
python examples/example_kokoro_hindi.py
```

---

## Adding New TTS Engines

1. Create folder: `tts_playground/new_engine/`
2. Implement `TTSBase` interface
3. Register in `tts_playground/factory.py`:

```python
TTS_ENGINES = {
    "xtts-hindi": XTTSHindi,
    "indri": IndriTTS,
    "kokoro": KokoroTTS,
    "new-engine": NewEngine,  # Add here
}
```

---

## Requirements

- **Python**: 3.9-3.11 (required)
- **PyTorch**: >= 2.0.0
- **Transformers**: 
  - XTTS: >= 4.35.0, < 4.40.0
  - Indri: >= 4.46.0
- **FFmpeg**: Required for XTTS on Windows
- **HuggingFace Token**: Required for model access

---

## License

MIT License

## Contributing

Contributions welcome! Please submit a Pull Request.

---

## Quick Reference

| Task | XTTS-Hindi | Indri | Kokoro |
|------|-----------|-------|--------|
| **Voice Cloning** | ✅ `speaker_wav="my_voice.wav"` | ❌ Not supported | ❌ Not supported |
| **Pre-trained Speakers** | ❌ Not available | ✅ `speaker="[spkr_68]"` | ✅ `voice="hf_alpha"` |
| **Languages** | Hindi only | English, Hindi, Code-mixing | Hindi |
| **Speed** | Slower | Faster | Very Fast |
| **Model Size** | Large | 350M | 82M |
| **Environment** | `venv` | `venv-indri` | `venv-kokoro` |
| **Python Version** | 3.9-3.11 | 3.9-3.11 | 3.10-3.12 |
| **Output Folder** | `output/xtts_hindi/` | `output/indri/` | `output/kokoro/` |

---

**For voice cloning**: Use XTTS-Hindi  
**For fast synthesis with variety**: Use Indri  
**For code-mixing**: Use Indri  
**For fastest Hindi TTS**: Use Kokoro
