# VibeVoice Hindi TTS - Google Colab Setup

## Quick Start (T4 GPU)

### Cell 1: Clone Repository
```python
!git clone https://github.com/kmarrrahulcode/tts-playground-hindi.git
%cd tts-playground-hindi
```

### Cell 2: Install VibeVoice Dependencies
```python
# Install VibeVoice from community fork FIRST
!pip install git+https://github.com/vibevoice-community/VibeVoice.git

# Install other dependencies
!pip install soundfile numpy huggingface_hub accelerate scipy librosa
!pip install fastapi uvicorn python-multipart

# System dependencies
!apt-get update && apt-get install -y ffmpeg
```

### Cell 3: Install TTS Playground (VibeVoice only)
```python
# Use --no-deps to avoid TTS library conflict
!pip install -e . --no-deps
```

### Cell 4: Test Basic Synthesis
```python
from tts_playground import get_tts_engine

# Initialize (uses CUDA automatically)
tts = get_tts_engine("vibevoice-hindi", device="cuda")
tts.initialize()

# Generate Hindi speech
text = "नमस्ते, मैं विबवॉइस हिंदी हूं।"
output = tts.synthesize(text=text, output_path="test.wav")
print(f"Generated: {output}")

# Play audio in Colab
from IPython.display import Audio
Audio(output)
```

---

## Alternative: One-Cell Setup

```python
# Complete setup in one cell
!git clone https://github.com/kmarrrahulcode/tts-playground-hindi.git
%cd tts-playground-hindi

# Install VibeVoice first
!pip install git+https://github.com/vibevoice-community/VibeVoice.git
!pip install soundfile numpy huggingface_hub accelerate
!apt-get update && apt-get install -y ffmpeg

# Install playground without deps (avoids TTS library conflict)
!pip install -e . --no-deps

# Test
from tts_playground import get_tts_engine
tts = get_tts_engine("vibevoice-hindi", device="cuda")
tts.initialize()
output = tts.synthesize(text="नमस्ते", output_path="test.wav")

from IPython.display import Audio
Audio(output)
```

---

## Voice Cloning

```python
# Upload your voice file first
from google.colab import files
uploaded = files.upload()  # Upload my_voice.wav

# Clone voice
output = tts.synthesize_with_voice(
    text="यह मेरी आवाज़ की क्लोनिंग है।",
    speaker_wav="my_voice.wav",
    output_path="cloned.wav"
)
Audio(output)
```

---

## Multi-Speaker Conversation

```python
dialogue = [
    {"speaker": "hi-Priya_woman", "text": "नमस्ते, कैसे हो?"},
    {"speaker": "hi-Raj_man", "text": "मैं ठीक हूं, धन्यवाद।"},
]

output = tts.synthesize_conversation(
    dialogue=dialogue,
    output_path="conversation.wav"
)
Audio(output)
```

---

## Available Speakers

| Speaker ID | Description |
|------------|-------------|
| `hi-Priya_woman` | Hindi Female - Calm, clear voice |
| `hi-Raj_man` | Hindi Male - Professional tone |
| `hi-Ananya_woman` | Hindi Female - Expressive voice |
| `hi-Vikram_man` | Hindi Male - Deep, authoritative |

---

## Troubleshooting

### "No matching distribution found for TTS>=0.22.0"
Use `--no-deps` flag:
```python
!pip install -e . --no-deps
```

### CUDA Out of Memory
```python
import torch
torch.cuda.empty_cache()
```

---

## Memory: T4 GPU (16GB)
- Model: ~6-8 GB VRAM
- Inference: ~2-4 GB additional
- Total: ~10-12 GB (fits on T4)
