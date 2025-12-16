# TTS Playground REST API

REST API for Text-to-Speech synthesis using XTTS-Hindi and Indri models.

## Quick Start

### 1. Install API Dependencies

```powershell
# Activate your environment (venv or venv-indri)
.\venv-indri\Scripts\Activate.ps1

# Install API requirements
pip install -r api/requirements.txt

# Set HuggingFace token
$env:HF_TOKEN="your_token_here"
```

### 2. Start the API Server

```powershell
cd api
python start_api.py
```

The API will be available at:
- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc

### 3. Test the API

```powershell
# In another terminal
python api/test_api.py
```

---

## API Endpoints

### Health Check

```bash
GET /health
```

**Response:**
```json
{
  "status": "healthy",
  "models_initialized": {
    "xtts-hindi": false,
    "indri": true
  }
}
```

### List Models

```bash
GET /models
```

**Response:**
```json
[
  {
    "name": "indri",
    "description": "Indri TTS with 13 pre-trained speakers",
    "languages": ["en", "hi", "code-mixing"],
    "features": ["fast", "multiple_speakers", "code_mixing"],
    "initialized": true
  }
]
```

### Get Speakers (Indri Only)

```bash
GET /speakers?model=indri
```

**Response:**
```json
{
  "model": "indri",
  "speakers": {
    "[spkr_68]": "🇮🇳 👨 book reader",
    "[spkr_70]": "🇮🇳 👨 motivational speaker",
    ...
  },
  "total": 13
}
```

### Synthesize Speech

```bash
POST /synthesize
Content-Type: application/json

{
  "text": "नमस्ते दोस्तों",
  "model": "indri",
  "output_filename": "hello.wav",
  "speaker": "[spkr_68]",
  "max_new_tokens": 2048
}
```

**Response:**
```json
{
  "success": true,
  "message": "Speech synthesized successfully",
  "output_path": "output/indri/hello.wav",
  "model_used": "indri",
  "file_size": 123456
}
```

### Synthesize with Voice Cloning (XTTS Only)

```bash
POST /synthesize-with-voice
Content-Type: multipart/form-data

text: "यह आपकी आवाज़ में बोल रहा है"
model: "xtts-hindi"
voice_file: <audio file>
language: "hi"
```

**Response:**
```json
{
  "success": true,
  "message": "Speech synthesized with voice cloning",
  "output_path": "output/xtts_hindi/cloned.wav",
  "model_used": "xtts-hindi",
  "file_size": 234567
}
```

### Download File

```bash
GET /download/{model}/{filename}
```

Example: `GET /download/indri/hello.wav`

Returns the audio file.

### Cleanup Files

```bash
DELETE /cleanup/{model}
```

- `model`: "indri", "xtts-hindi", or "all"

**Response:**
```json
{
  "success": true,
  "message": "Deleted 5 files",
  "models_cleaned": ["indri"]
}
```

---

## Usage Examples

### Python (requests)

```python
import requests

# Synthesize with Indri
response = requests.post("http://localhost:8000/synthesize", json={
    "text": "नमस्ते दोस्तों",
    "model": "indri",
    "speaker": "[spkr_68]",
    "max_new_tokens": 4096
})

result = response.json()
print(f"Audio saved to: {result['output_path']}")

# Download the file
audio_response = requests.get(f"http://localhost:8000/download/indri/hello.wav")
with open("downloaded.wav", "wb") as f:
    f.write(audio_response.content)
```

### cURL

```bash
# Synthesize with Indri
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{
    "text": "नमस्ते दोस्तों",
    "model": "indri",
    "speaker": "[spkr_68]",
    "max_new_tokens": 2048
  }'

# Get speakers
curl "http://localhost:8000/speakers?model=indri"

# Download file
curl "http://localhost:8000/download/indri/hello.wav" -o hello.wav

# Voice cloning with XTTS
curl -X POST "http://localhost:8000/synthesize-with-voice" \
  -F "text=यह आपकी आवाज़ में है" \
  -F "model=xtts-hindi" \
  -F "voice_file=@my_voice.wav" \
  -F "language=hi"
```

### PowerShell

```powershell
# Synthesize with Indri
$body = @{
    text = "नमस्ते दोस्तों"
    model = "indri"
    speaker = "[spkr_68]"
    max_new_tokens = 2048
} | ConvertTo-Json

Invoke-RestMethod -Uri "http://localhost:8000/synthesize" `
    -Method Post `
    -ContentType "application/json" `
    -Body $body

# Download file
Invoke-WebRequest -Uri "http://localhost:8000/download/indri/hello.wav" `
    -OutFile "hello.wav"
```

### JavaScript (fetch)

```javascript
// Synthesize with Indri
fetch('http://localhost:8000/synthesize', {
  method: 'POST',
  headers: {
    'Content-Type': 'application/json',
  },
  body: JSON.stringify({
    text: 'नमस्ते दोस्तों',
    model: 'indri',
    speaker: '[spkr_68]',
    max_new_tokens: 2048
  })
})
.then(response => response.json())
.then(data => console.log('Audio saved to:', data.output_path));

// Voice cloning with XTTS
const formData = new FormData();
formData.append('text', 'यह आपकी आवाज़ में है');
formData.append('model', 'xtts-hindi');
formData.append('voice_file', fileInput.files[0]);
formData.append('language', 'hi');

fetch('http://localhost:8000/synthesize-with-voice', {
  method: 'POST',
  body: formData
})
.then(response => response.json())
.then(data => console.log('Cloned audio:', data.output_path));
```

---

## Request Parameters

### Synthesize Endpoint

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | Yes | - | Text to convert to speech |
| `model` | string | Yes | "indri" | "xtts-hindi" or "indri" |
| `output_filename` | string | No | Auto-generated | Output filename |
| `speaker` | string | No | "[spkr_68]" | Speaker ID (Indri only) |
| `language` | string | No | "hi" | Language code (XTTS only) |
| `max_new_tokens` | int | No | 2048 | Max tokens (Indri only) |
| `temperature` | float | No | 1.0 | Sampling temperature |
| `use_default_output_dir` | bool | No | true | Use output/model/ folder |

### Voice Cloning Endpoint

| Parameter | Type | Required | Default | Description |
|-----------|------|----------|---------|-------------|
| `text` | string | Yes | - | Text to convert to speech |
| `model` | string | Yes | "xtts-hindi" | Must be "xtts-hindi" |
| `voice_file` | file | Yes | - | Audio file (3-10 seconds) |
| `output_filename` | string | No | Auto-generated | Output filename |
| `language` | string | No | "hi" | Language code |
| `use_default_output_dir` | bool | No | true | Use output/model/ folder |

---

## Error Handling

The API returns standard HTTP status codes:

- **200**: Success
- **400**: Bad request (invalid parameters)
- **404**: Not found (file doesn't exist)
- **500**: Server error (model initialization failed, etc.)

**Error Response:**
```json
{
  "detail": "Error message here"
}
```

---

## Performance Notes

- **First Request**: Slower (model initialization)
- **Subsequent Requests**: Faster (model cached in memory)
- **Indri**: ~2-5 seconds per request
- **XTTS**: ~5-10 seconds per request
- **Voice Cloning**: Additional 1-2 seconds for file upload

---

## Deployment

### Production Deployment

For production, use a proper ASGI server:

```bash
# Install production server
pip install gunicorn

# Run with gunicorn
gunicorn api.main:app -w 4 -k uvicorn.workers.UvicornWorker -b 0.0.0.0:8000
```

### Docker Deployment

```dockerfile
FROM python:3.11-slim

WORKDIR /app
COPY . /app

RUN pip install -r requirements.txt
RUN pip install -r api/requirements.txt
RUN pip install -e .

ENV HF_TOKEN=""
EXPOSE 8000

CMD ["python", "api/start_api.py"]
```

---

## Security Considerations

⚠️ **Important for Production:**

1. **Authentication**: Add API key authentication
2. **Rate Limiting**: Implement rate limiting
3. **File Size Limits**: Limit upload file sizes
4. **CORS**: Configure CORS for web clients
5. **HTTPS**: Use HTTPS in production
6. **Input Validation**: Validate all inputs
7. **Resource Limits**: Set memory/CPU limits

---

## Troubleshooting

### API Won't Start

**Problem**: `ModuleNotFoundError: No module named 'tts_playground'`

**Solution**: Make sure you're in the correct directory and the package is installed:
```powershell
cd C:\path\to\TTS-Playground
pip install -e .
python api/start_api.py
```

### Model Initialization Fails

**Problem**: `Failed to initialize model`

**Solution**: 
1. Check HF_TOKEN is set
2. Ensure correct environment is activated
3. Check internet connection for model download

### Voice Cloning Doesn't Work

**Problem**: `Voice cloning only supported with 'xtts-hindi'`

**Solution**: Use XTTS-Hindi model, not Indri. Indri only supports pre-trained speakers.

---

## Interactive API Documentation

Once the server is running, visit:

- **Swagger UI**: http://localhost:8000/docs
  - Interactive API testing
  - Try out endpoints directly
  - See request/response schemas

- **ReDoc**: http://localhost:8000/redoc
  - Clean documentation
  - Better for reading

---

## License

MIT License - Same as TTS Playground
