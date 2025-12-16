"""
Startup script for TTS Playground API
"""
import sys
import os
import uvicorn
from pathlib import Path

# Add parent directory to path to import tts_playground
sys.path.insert(0, str(Path(__file__).parent.parent))

# Set HF_TOKEN if not already set
if not os.getenv("HF_TOKEN"):
    print("Warning: HF_TOKEN environment variable not set!")
    print("Set it with: $env:HF_TOKEN='your_token_here'")

import uvicorn

if __name__ == "__main__":
    print("=" * 60)
    print("TTS Playground REST API")
    print("=" * 60)
    print("\nStarting server...")
    print("API URL: http://localhost:8000")
    print("API Docs: http://localhost:8000/docs")
    print("Interactive API: http://localhost:8000/redoc")
    print("\nPress Ctrl+C to stop")
    print("=" * 60)
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True,
        log_level="info"
    )
