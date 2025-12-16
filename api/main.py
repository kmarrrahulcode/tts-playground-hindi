"""
TTS Playground REST API
FastAPI server to expose TTS functionality
"""

import os
import shutil
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException, UploadFile, File, Form
from fastapi.responses import FileResponse, JSONResponse
from pydantic import BaseModel, Field
import uvicorn

from tts_playground import get_tts_engine

# Initialize FastAPI app
app = FastAPI(
    title="TTS Playground API",
    description="REST API for Text-to-Speech with XTTS-Hindi and Indri models",
    version="1.0.0"
)

# Store initialized engines
engines = {}

# Temporary upload directory
UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class TTSRequest(BaseModel):
    """Request model for TTS synthesis"""
    text: str = Field(..., description="Text to convert to speech")
    model: str = Field("indri", description="Model to use: 'xtts-hindi' or 'indri'")
    output_filename: Optional[str] = Field(None, description="Output filename (without path)")
    speaker: Optional[str] = Field(None, description="Speaker ID for Indri (e.g., '[spkr_68]')")
    language: Optional[str] = Field("hi", description="Language code (for XTTS)")
    max_new_tokens: Optional[int] = Field(2048, description="Max tokens for Indri (2048-16384)")
    temperature: Optional[float] = Field(1.0, description="Sampling temperature (0.7-1.3)")
    use_default_output_dir: Optional[bool] = Field(True, description="Use output/model_name/ folder")


class TTSResponse(BaseModel):
    """Response model for TTS synthesis"""
    success: bool
    message: str
    output_path: Optional[str] = None
    model_used: str
    file_size: Optional[int] = None


class ModelInfo(BaseModel):
    """Model information"""
    name: str
    description: str
    languages: List[str]
    features: List[str]
    initialized: bool


@app.on_event("startup")
async def startup_event():
    """Initialize models on startup"""
    print("TTS Playground API starting...")
    print("Models will be initialized on first use")


@app.on_event("shutdown")
async def shutdown_event():
    """Cleanup on shutdown"""
    print("Shutting down TTS Playground API...")
    # Clean up temp uploads
    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR)


@app.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "name": "TTS Playground API",
        "version": "1.0.0",
        "models": ["xtts-hindi", "indri"],
        "endpoints": {
            "POST /synthesize": "Synthesize speech from text",
            "POST /synthesize-with-voice": "Synthesize with voice cloning (XTTS only)",
            "GET /models": "List available models",
            "GET /speakers": "Get available speakers (Indri only)",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "models_initialized": {
            "xtts-hindi": "xtts-hindi" in engines,
            "indri": "indri" in engines
        }
    }


@app.get("/models", response_model=List[ModelInfo])
async def list_models():
    """List available TTS models"""
    return [
        ModelInfo(
            name="xtts-hindi",
            description="XTTS-Hindi with voice cloning support",
            languages=["hi"],
            features=["voice_cloning", "high_quality"],
            initialized="xtts-hindi" in engines
        ),
        ModelInfo(
            name="indri",
            description="Indri TTS with 13 pre-trained speakers",
            languages=["en", "hi", "code-mixing"],
            features=["fast", "multiple_speakers", "code_mixing"],
            initialized="indri" in engines
        )
    ]


@app.get("/speakers")
async def get_speakers(model: str = "indri"):
    """Get available speakers for a model"""
    if model != "indri":
        raise HTTPException(
            status_code=400,
            detail="Only 'indri' model has pre-trained speakers. Use voice cloning for XTTS."
        )
    
    # Initialize Indri if not already done
    if "indri" not in engines:
        try:
            engines["indri"] = get_tts_engine("indri", device="cpu")
            engines["indri"].initialize()
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize Indri: {str(e)}")
    
    speakers = engines["indri"].get_available_speakers()
    return {
        "model": "indri",
        "speakers": speakers,
        "total": len(speakers)
    }


def get_or_initialize_engine(model_name: str):
    """Get or initialize a TTS engine"""
    if model_name not in ["xtts-hindi", "indri"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model: {model_name}. Choose 'xtts-hindi' or 'indri'"
        )
    
    if model_name not in engines:
        try:
            print(f"Initializing {model_name} model...")
            engines[model_name] = get_tts_engine(model_name, device="cpu")
            engines[model_name].initialize()
            print(f"{model_name} model initialized successfully")
        except Exception as e:
            raise HTTPException(
                status_code=500,
                detail=f"Failed to initialize {model_name}: {str(e)}"
            )
    
    return engines[model_name]


@app.post("/synthesize", response_model=TTSResponse)
async def synthesize_speech(request: TTSRequest):
    """
    Synthesize speech from text
    
    - **text**: Text to convert to speech
    - **model**: 'xtts-hindi' or 'indri'
    - **output_filename**: Optional output filename
    - **speaker**: Speaker ID for Indri (e.g., '[spkr_68]')
    - **language**: Language code for XTTS (default: 'hi')
    - **max_new_tokens**: Max tokens for Indri (default: 2048)
    - **temperature**: Sampling temperature (default: 1.0)
    """
    try:
        # Get or initialize engine
        tts = get_or_initialize_engine(request.model)
        
        # Prepare output filename
        if request.output_filename:
            output_path = request.output_filename
        else:
            # Generate filename from text
            safe_text = "".join(c for c in request.text[:30] if c.isalnum() or c in (' ', '-', '_'))
            safe_text = safe_text.replace(' ', '_')
            output_path = f"{safe_text}.wav"
        
        # Prepare synthesis parameters
        synth_params = {
            "text": request.text,
            "output_path": output_path,
            "use_default_output_dir": request.use_default_output_dir
        }
        
        # Model-specific parameters
        if request.model == "indri":
            if request.speaker:
                synth_params["speaker"] = request.speaker
            synth_params["max_new_tokens"] = request.max_new_tokens
            synth_params["temperature"] = request.temperature
        elif request.model == "xtts-hindi":
            synth_params["language"] = request.language
        
        # Synthesize
        result_path = tts.synthesize(**synth_params)
        
        # Get file size
        file_size = Path(result_path).stat().st_size if Path(result_path).exists() else None
        
        return TTSResponse(
            success=True,
            message="Speech synthesized successfully",
            output_path=result_path,
            model_used=request.model,
            file_size=file_size
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/synthesize-with-voice")
async def synthesize_with_voice(
    text: str = Form(...),
    model: str = Form("xtts-hindi"),
    voice_file: UploadFile = File(...),
    output_filename: Optional[str] = Form(None),
    language: str = Form("hi"),
    use_default_output_dir: bool = Form(True)
):
    """
    Synthesize speech with voice cloning (XTTS-Hindi only)
    
    - **text**: Text to convert to speech
    - **model**: Must be 'xtts-hindi' (Indri doesn't support voice cloning)
    - **voice_file**: Audio file with voice sample (3-10 seconds)
    - **output_filename**: Optional output filename
    - **language**: Language code (default: 'hi')
    """
    if model != "xtts-hindi":
        raise HTTPException(
            status_code=400,
            detail="Voice cloning only supported with 'xtts-hindi' model. Use 'indri' with pre-trained speakers."
        )
    
    try:
        # Get or initialize engine
        tts = get_or_initialize_engine(model)
        
        # Save uploaded voice file
        voice_path = UPLOAD_DIR / voice_file.filename
        with open(voice_path, "wb") as f:
            content = await voice_file.read()
            f.write(content)
        
        # Prepare output filename
        if output_filename:
            output_path = output_filename
        else:
            safe_text = "".join(c for c in text[:30] if c.isalnum() or c in (' ', '-', '_'))
            safe_text = safe_text.replace(' ', '_')
            output_path = f"{safe_text}_cloned.wav"
        
        # Synthesize with voice cloning
        result_path = tts.synthesize(
            text=text,
            output_path=output_path,
            speaker_wav=str(voice_path),
            language=language,
            use_default_output_dir=use_default_output_dir
        )
        
        # Clean up uploaded file
        voice_path.unlink()
        
        # Get file size
        file_size = Path(result_path).stat().st_size if Path(result_path).exists() else None
        
        return TTSResponse(
            success=True,
            message="Speech synthesized with voice cloning",
            output_path=result_path,
            model_used=model,
            file_size=file_size
        )
        
    except Exception as e:
        # Clean up on error
        if voice_path.exists():
            voice_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{model}/{filename}")
async def download_file(model: str, filename: str):
    """
    Download generated audio file
    
    - **model**: 'xtts-hindi' or 'indri'
    - **filename**: Name of the file to download
    """
    file_path = Path("output") / model / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(
        path=file_path,
        media_type="audio/wav",
        filename=filename
    )


@app.delete("/cleanup/{model}")
async def cleanup_outputs(model: str):
    """
    Clean up output files for a model
    
    - **model**: 'xtts-hindi' or 'indri' or 'all'
    """
    try:
        if model == "all":
            models = ["xtts-hindi", "indri"]
        elif model in ["xtts-hindi", "indri"]:
            models = [model]
        else:
            raise HTTPException(status_code=400, detail="Invalid model")
        
        deleted_count = 0
        for m in models:
            output_dir = Path("output") / m
            if output_dir.exists():
                for file in output_dir.glob("*.wav"):
                    file.unlink()
                    deleted_count += 1
        
        return {
            "success": True,
            "message": f"Deleted {deleted_count} files",
            "models_cleaned": models
        }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    # Run the API server
    print("Starting TTS Playground API...")
    print("API will be available at: http://localhost:8000")
    print("API docs at: http://localhost:8000/docs")
    
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )
