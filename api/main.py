"""
TTS Playground REST API
FastAPI server to expose TTS functionality
"""

import os
import shutil
import json
import time
from pathlib import Path
from typing import Optional, List
from fastapi import FastAPI, HTTPException, UploadFile, File, Form, Request
from fastapi.responses import FileResponse, JSONResponse, Response
from starlette.middleware.base import BaseHTTPMiddleware
from pydantic import BaseModel, Field
import uvicorn

from tts_playground import get_tts_engine


class RequestResponseLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware to log raw requests and error responses"""
    
    async def dispatch(self, request: Request, call_next):
        request_time = time.strftime("%Y-%m-%d %H:%M:%S")
        method = request.method
        url = str(request.url)
        headers = dict(request.headers)
        
        body = await request.body()
        body_str = body.decode("utf-8") if body else ""
        
        print("\n" + "=" * 60)
        print(f"[{request_time}] RAW REQUEST")
        print("=" * 60)
        print(f"Method: {method}")
        print(f"URL: {url}")
        print(f"Headers: {json.dumps({k: v for k, v in headers.items() if k.lower() not in ['authorization', 'cookie']}, indent=2)}")
        if body_str:
            try:
                body_json = json.loads(body_str)
                print(f"Body: {json.dumps(body_json, indent=2, ensure_ascii=False)}")
            except json.JSONDecodeError:
                print(f"Body: {body_str[:500]}{'...' if len(body_str) > 500 else ''}")
        print("=" * 60)
        
        async def receive():
            return {"type": "http.request", "body": body}
        request._receive = receive
        
        response = await call_next(request)
        
        if response.status_code >= 400:
            response_body = b""
            async for chunk in response.body_iterator:
                response_body += chunk
            
            response_str = response_body.decode("utf-8") if response_body else ""
            
            print("\n" + "!" * 60)
            print(f"[{request_time}] ERROR RESPONSE ({response.status_code})")
            print("!" * 60)
            print(f"Status: {response.status_code}")
            if response_str:
                try:
                    response_json = json.loads(response_str)
                    print(f"Response: {json.dumps(response_json, indent=2, ensure_ascii=False)}")
                except json.JSONDecodeError:
                    print(f"Response: {response_str[:500]}{'...' if len(response_str) > 500 else ''}")
            print("!" * 60 + "\n")
            
            return Response(
                content=response_body,
                status_code=response.status_code,
                headers=dict(response.headers),
                media_type=response.media_type
            )
        
        return response


app = FastAPI(
    title="TTS Playground API",
    description="REST API for Text-to-Speech with XTTS-Hindi and Indic Parler models",
    version="1.0.0"
)

app.add_middleware(RequestResponseLoggingMiddleware)

engines = {}
UPLOAD_DIR = Path("temp_uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


class TTSRequest(BaseModel):
    """Request model for TTS synthesis"""
    text: str = Field(..., description="Text to convert to speech")
    model: str = Field("indic-parler", description="Model: 'xtts-hindi', 'indic-parler', 'kokoro', or 'f5-hindi'")
    output_filename: Optional[str] = Field(None, description="Output filename")
    language: Optional[str] = Field("hi", description="Language code (for XTTS)")
    use_default_output_dir: Optional[bool] = Field(True, description="Use output/model_name/ folder")
    description: Optional[str] = Field(None, description="Voice description for Indic Parler")
    voice: Optional[str] = Field(None, description="Voice ID for Kokoro (hf_alpha, hf_beta, hm_omega, hm_psi)")
    speed: Optional[float] = Field(1.0, description="Speech speed for Kokoro (0.5-2.0)")
    ref_text: Optional[str] = Field(None, description="Reference audio transcript for F5-Hindi")


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
    print("TTS Playground API starting...")
    print("Models will be initialized on first use")


@app.on_event("shutdown")
async def shutdown_event():
    print("Shutting down TTS Playground API...")
    if UPLOAD_DIR.exists():
        shutil.rmtree(UPLOAD_DIR)


@app.get("/")
async def root():
    return {
        "name": "TTS Playground API",
        "version": "1.0.0",
        "models": ["xtts-hindi", "indic-parler", "kokoro", "f5-hindi"],
        "endpoints": {
            "POST /synthesize": "Synthesize speech from text",
            "POST /synthesize-with-voice": "Synthesize with voice cloning (XTTS, F5-Hindi)",
            "GET /models": "List available models",
            "GET /speakers": "Get speakers/voices for a model",
            "GET /voices": "Get voice descriptions (Indic Parler)",
            "GET /health": "Health check"
        }
    }


@app.get("/health")
async def health_check():
    return {
        "status": "healthy",
        "models_initialized": {
            "xtts-hindi": "xtts-hindi" in engines,
            "indic-parler": "indic-parler" in engines,
            "kokoro": "kokoro" in engines,
            "f5-hindi": "f5-hindi" in engines
        }
    }


@app.get("/models", response_model=List[ModelInfo])
async def list_models():
    return [
        ModelInfo(
            name="xtts-hindi",
            description="XTTS-Hindi with voice cloning support",
            languages=["hi"],
            features=["voice_cloning", "high_quality"],
            initialized="xtts-hindi" in engines
        ),
        ModelInfo(
            name="indic-parler",
            description="Indic Parler TTS with 22 Indian languages",
            languages=["hi", "ta", "te", "bn", "mr", "gu", "kn", "ml", "pa", "or", "as", "en", "ne", "sa", "sd", "ks", "doi", "mai", "mni", "sat", "brx", "gom"],
            features=["voice_description", "multilingual", "22_languages"],
            initialized="indic-parler" in engines
        ),
        ModelInfo(
            name="kokoro",
            description="Kokoro TTS - Fast, lightweight Hindi TTS (82M model)",
            languages=["hi"],
            features=["fast", "lightweight", "multiple_voices"],
            initialized="kokoro" in engines
        ),
        ModelInfo(
            name="f5-hindi",
            description="F5-Hindi TTS - High-quality voice cloning for Hindi (SPRINGLab)",
            languages=["hi"],
            features=["voice_cloning", "high_quality", "24khz"],
            initialized="f5-hindi" in engines
        )
    ]


@app.get("/voices")
async def get_voice_descriptions():
    return {
        "model": "indic-parler",
        "example_descriptions": {
            "female_calm": "A female speaker with a calm and clear voice.",
            "male_calm": "A male speaker with a calm and clear voice.",
            "female_expressive": "A female speaker with an expressive and energetic voice.",
            "male_expressive": "A male speaker with an expressive and energetic voice.",
        },
        "supported_languages": {
            "as": "Assamese", "bn": "Bengali", "brx": "Bodo", "doi": "Dogri",
            "en": "English", "gom": "Konkani", "gu": "Gujarati", "hi": "Hindi",
            "kn": "Kannada", "ks": "Kashmiri", "mai": "Maithili", "ml": "Malayalam",
            "mni": "Manipuri", "mr": "Marathi", "ne": "Nepali", "or": "Odia",
            "pa": "Punjabi", "sa": "Sanskrit", "sat": "Santali", "sd": "Sindhi",
            "ta": "Tamil", "te": "Telugu"
        }
    }


@app.get("/speakers")
async def get_speakers(model: str = "kokoro"):
    """Get available speakers/voices for a model"""
    if model == "kokoro":
        return {
            "model": "kokoro",
            "voices": {
                "hf_alpha": "Hindi Female Alpha",
                "hf_beta": "Hindi Female Beta",
                "hm_omega": "Hindi Male Omega",
                "hm_psi": "Hindi Male Psi"
            },
            "total": 4
        }
    elif model == "indic-parler":
        return {
            "model": "indic-parler",
            "voices": {
                "female_calm": "A female speaker with a calm and clear voice.",
                "male_calm": "A male speaker with a calm and clear voice.",
                "female_expressive": "A female speaker with an expressive and energetic voice.",
                "male_expressive": "A male speaker with an expressive and energetic voice.",
            },
            "total": 4
        }
    elif model == "xtts-hindi":
        return {
            "model": "xtts-hindi",
            "voices": {},
            "note": "XTTS-Hindi uses voice cloning. Upload your own voice file.",
            "total": 0
        }
    elif model == "f5-hindi":
        return {
            "model": "f5-hindi",
            "voices": {},
            "note": "F5-Hindi uses voice cloning. Upload your own voice file via /synthesize-with-voice endpoint.",
            "total": 0
        }
    else:
        raise HTTPException(status_code=400, detail=f"Unknown model: {model}")


def get_or_initialize_engine(model_name: str):
    if model_name not in ["xtts-hindi", "indic-parler", "kokoro", "f5-hindi"]:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid model: {model_name}. Choose 'xtts-hindi', 'indic-parler', 'kokoro', or 'f5-hindi'"
        )
    
    if model_name not in engines:
        try:
            print(f"Initializing {model_name} model...")
            engines[model_name] = get_tts_engine(model_name, device="cpu")
            engines[model_name].initialize()
            print(f"{model_name} model initialized successfully")
        except Exception as e:
            raise HTTPException(status_code=500, detail=f"Failed to initialize {model_name}: {str(e)}")
    
    return engines[model_name]


@app.post("/synthesize", response_model=TTSResponse)
async def synthesize_speech(request: TTSRequest):
    try:
        tts = get_or_initialize_engine(request.model)
        
        if request.output_filename:
            output_path = request.output_filename
        else:
            safe_text = "".join(c for c in request.text[:30] if c.isalnum() or c in (' ', '-', '_'))
            safe_text = safe_text.replace(' ', '_')
            output_path = f"{safe_text}.wav"
        
        synth_params = {
            "text": request.text,
            "output_path": output_path,
            "use_default_output_dir": request.use_default_output_dir
        }
        
        if request.model == "xtts-hindi":
            synth_params["language"] = request.language
        elif request.model == "indic-parler":
            if request.description:
                synth_params["description"] = request.description
        elif request.model == "kokoro":
            if request.voice:
                synth_params["voice"] = request.voice
            if request.speed:
                synth_params["speed"] = request.speed
        
        result_path = tts.synthesize(**synth_params)
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
    use_default_output_dir: bool = Form(True),
    ref_text: Optional[str] = Form(None)
):
    if model not in ["xtts-hindi", "f5-hindi"]:
        raise HTTPException(
            status_code=400,
            detail="Voice cloning only supported with 'xtts-hindi' or 'f5-hindi' models."
        )
    
    try:
        tts = get_or_initialize_engine(model)
        
        voice_path = UPLOAD_DIR / voice_file.filename
        with open(voice_path, "wb") as f:
            content = await voice_file.read()
            f.write(content)
        
        if output_filename:
            output_path = output_filename
        else:
            safe_text = "".join(c for c in text[:30] if c.isalnum() or c in (' ', '-', '_'))
            safe_text = safe_text.replace(' ', '_')
            output_path = f"{safe_text}_cloned.wav"
        
        synth_params = {
            "text": text,
            "output_path": output_path,
            "speaker_wav": str(voice_path),
            "use_default_output_dir": use_default_output_dir
        }
        
        if model == "xtts-hindi":
            synth_params["language"] = language
        elif model == "f5-hindi":
            if ref_text:
                synth_params["ref_text"] = ref_text
        
        result_path = tts.synthesize(**synth_params)
        
        voice_path.unlink()
        file_size = Path(result_path).stat().st_size if Path(result_path).exists() else None
        
        return TTSResponse(
            success=True,
            message="Speech synthesized with voice cloning",
            output_path=result_path,
            model_used=model,
            file_size=file_size
        )
        
    except Exception as e:
        if voice_path.exists():
            voice_path.unlink()
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/download/{model}/{filename}")
async def download_file(model: str, filename: str):
    file_path = Path("output") / model / filename
    
    if not file_path.exists():
        raise HTTPException(status_code=404, detail="File not found")
    
    return FileResponse(path=file_path, media_type="audio/wav", filename=filename)


@app.delete("/cleanup/{model}")
async def cleanup_outputs(model: str):
    try:
        if model == "all":
            models = ["xtts_hindi", "indic_parler", "kokoro", "f5_hindi"]
        elif model in ["xtts-hindi", "indic-parler", "kokoro", "f5-hindi"]:
            models = [model.replace("-", "_")]
        else:
            raise HTTPException(status_code=400, detail="Invalid model")
        
        deleted_count = 0
        for m in models:
            output_dir = Path("output") / m
            if output_dir.exists():
                for file in output_dir.glob("*.wav"):
                    file.unlink()
                    deleted_count += 1
        
        return {"success": True, "message": f"Deleted {deleted_count} files", "models_cleaned": models}
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    print("Starting TTS Playground API...")
    print("API will be available at: http://localhost:8000")
    print("API docs at: http://localhost:8000/docs")
    
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
