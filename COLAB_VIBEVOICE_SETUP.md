# VibeVoice Hindi TTS - Google Colab Setup

## Quick Start (T4 GPU)

### Cell 1: Clone Repository
```python
!git clone https://github.com/your-repo/tts-playground.git
%cd tts-playground
```

### Cell 2: Install Dependencies
```python
# Install VibeVoice from community fork
!pip install git+https://github.com/vibevoice-community/VibeVoice.git

# Install other dependencies
!pip install soundfile numpy huggingface_hub accelerate scipy librosa
!pip install fastapi uvicorn python-multipart

# Install tts-playground
!pip install -e .

# System dependencies
!apt-get update && apt-get install -y ffmpeg
```

### Cell 3: Test Basic Synthesis
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

### Cell 4: Voice Cloning (Optional)
```python
# Upload your voice file first
from google.colab import files
uploaded = files.upload()  # Upload my_voice.wav

# Clone voice
text = "यह मेरी आवाज़ की क्लोनिंग है।"
output = tts.synthesize_with_voice(
    text=text,
    speaker_wav="my_voice.wav",
    output_path="cloned.wav"
)
Audio(output)
```

### Cell 5: Multi-Speaker Conversation
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

## API Server in Colab

### Cell 1: Start API with ngrok
```python
!pip install pyngrok

from pyngrok import ngrok
ngrok.set_auth_token("YOUR_NGROK_TOKEN")  # Get from ngrok.com

# Start tunnel
public_url = ngrok.connect(8000)
print(f"API URL: {public_url}")
print(f"Docs: {public_url}/docs")
```

### Cell 2: Run API Server
```python
%cd api
!python start_api.py
```

---

## Available Speakers

| Speaker ID | Description |
|------------|-------------|
| `hi-Priya_woman` | Hindi Female (Priya) - Calm, clear voice |
| `hi-Raj_man` | Hindi Male (Raj) - Professional tone |
| `hi-Ananya_woman` | Hindi Female (Ananya) - Expressive voice |
| `hi-Vikram_man` | Hindi Male (Vikram) - Deep, authoritative |

---

## API Endpoints

| Endpoint | Method | Description |
|----------|--------|-------------|
| `/synthesize` | POST | Basic TTS with speaker selection |
| `/synthesize-with-voice` | POST | Voice cloning |
| `/speakers?model=vibevoice-hindi` | GET | List speakers |
| `/health` | GET | Health check |

### Example API Call
```python
import requests

response = requests.post(
    f"{public_url}/synthesize",
    json={
        "text": "नमस्ते दुनिया",
        "model": "vibevoice-hindi",
        "speaker": "hi-Priya_woman"
    }
)
print(response.json())
```

---

## Memory Usage (T4 GPU - 16GB)

- Model loading: ~6-8 GB VRAM
- Inference: ~2-4 GB additional
- Recommended: Keep batch sizes small for long texts

## Tips

1. Use `torch.float16` (default) for memory efficiency
2. Set `seed` parameter for reproducible outputs
3. Adjust `cfg_scale` (1.0-2.0) for voice fidelity
4. For voice cloning, use 5-15 second reference audio
