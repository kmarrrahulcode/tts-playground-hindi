# Quick Start - TTS Playground REST API

## 5-Minute Setup

### Step 1: Install API Dependencies (1 minute)

```powershell
# Activate your environment
.\venv-indri\Scripts\Activate.ps1

# Install API requirements
pip install -r api/requirements.txt
```

### Step 2: Set Environment Variable (30 seconds)

```powershell
$env:HF_TOKEN="your_huggingface_token_here"
```

### Step 3: Start the Server (30 seconds)

```powershell
cd api
python start_api.py
```

You should see:
```
TTS Playground REST API
============================================================
Starting server...
API URL: http://localhost:8000
API Docs: http://localhost:8000/docs
```

### Step 4: Test the API (3 minutes)

**Option A: Use the Web Client**

1. Open `api/example_client.html` in your browser
2. Enter text: "नमस्ते दोस्तों"
3. Click "Generate Speech"
4. Listen to the audio!

**Option B: Use Interactive Docs**

1. Open http://localhost:8000/docs
2. Click on "POST /synthesize"
3. Click "Try it out"
4. Enter:
   ```json
   {
     "text": "नमस्ते दोस्तों",
     "model": "indri",
     "speaker": "[spkr_68]"
   }
   ```
5. Click "Execute"

**Option C: Use Python**

```python
import requests

response = requests.post("http://localhost:8000/synthesize", json={
    "text": "नमस्ते दोस्तों",
    "model": "indri",
    "speaker": "[spkr_68]"
})

print(response.json())
```

**Option D: Use cURL**

```bash
curl -X POST "http://localhost:8000/synthesize" \
  -H "Content-Type: application/json" \
  -d '{"text": "नमस्ते दोस्तों", "model": "indri"}'
```

## That's It!

Your TTS API is now running and ready to use!

## Next Steps

- **Explore Models**: Try both "indri" and "xtts-hindi"
- **Try Speakers**: Use different speakers with Indri
- **Voice Cloning**: Upload a voice sample with XTTS
- **Read Docs**: Check `api/README_API.md` for complete documentation
- **Integrate**: Use the API in your applications

## Common Commands

```powershell
# Start server
cd api
python start_api.py

# Test API
python api/test_api.py

# Stop server
Ctrl+C
```

## Troubleshooting

**Problem**: `ModuleNotFoundError: No module named 'fastapi'`  
**Solution**: `pip install -r api/requirements.txt`

**Problem**: `ModuleNotFoundError: No module named 'tts_playground'`  
**Solution**: `pip install -e .` (from project root)

**Problem**: Model initialization fails  
**Solution**: Check `$env:HF_TOKEN` is set correctly

## URLs

- **API**: http://localhost:8000
- **Interactive Docs**: http://localhost:8000/docs
- **ReDoc**: http://localhost:8000/redoc
- **Health Check**: http://localhost:8000/health

Enjoy! 🎉
