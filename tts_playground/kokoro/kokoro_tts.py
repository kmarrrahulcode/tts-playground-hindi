"""
Kokoro TTS Implementation
Text-to-speech with Hindi support using hexgrad/kokoro
"""

import os
import soundfile as sf
from pathlib import Path
from typing import Optional, Union, List

from tts_playground.base import TTSBase


class KokoroTTS(TTSBase):
    """
    Kokoro TTS Engine
    
    Model: hexgrad/Kokoro-82M
    Supports: Multiple languages including Hindi
    Features: Fast, lightweight, high-quality TTS
    """
    
    # Hindi voices available in Kokoro
    # hf_ = Hindi Female, hm_ = Hindi Male
    HINDI_VOICES = {
        "hf_alpha": "Hindi Female Alpha",
        "hf_beta": "Hindi Female Beta",
        "hm_omega": "Hindi Male Omega",
        "hm_psi": "Hindi Male Psi",
    }
    
    # Supported languages (focusing on Hindi as requested)
    SUPPORTED_LANGUAGES = {
        "hi": "Hindi",
    }
    
    def __init__(self, model_name: str = "hexgrad/Kokoro-82M",
                 device: str = "cpu", voice: str = "hf_alpha"):
        """
        Initialize Kokoro TTS engine
        
        Args:
            model_name: HuggingFace model name
            device: Device to run on ('cpu' or 'cuda')
            voice: Voice ID to use (default: hf_alpha for Hindi female)
        """
        super().__init__(model_name, device)
        self.voice = voice
        self._pipeline = None

    def initialize(self):
        """Initialize the Kokoro TTS pipeline"""
        if self._initialized:
            return
        
        try:
            print(f"Loading Kokoro TTS model: {self.model_name}")
            print(f"Device: {self.device}")
            print(f"Voice: {self.voice}")
            
            from kokoro import KPipeline
            
            # Initialize pipeline with Hindi language
            # lang_code 'h' is for Hindi in Kokoro
            self._pipeline = KPipeline(lang_code='h', device=self.device)
            
            self._initialized = True
            print("Kokoro TTS model loaded successfully!")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Kokoro TTS: {str(e)}")

    def synthesize(self, text: str, output_path: Optional[Union[str, Path]] = None,
                   voice: Optional[str] = None,
                   speed: float = 1.0,
                   use_default_output_dir: bool = True,
                   **kwargs) -> Union[bytes, str]:
        """
        Synthesize speech from text
        
        Args:
            text: Text to convert to speech (Hindi text supported)
            output_path: Optional path to save audio file (if None, returns bytes)
            voice: Voice ID override (default uses instance voice)
            speed: Speech speed multiplier (default 1.0)
            use_default_output_dir: Use output/kokoro/ folder structure
            **kwargs: Additional generation parameters
            
        Returns:
            Path to saved file if output_path provided, else audio bytes
        """
        if not self._initialized:
            self.initialize()
        
        try:
            # Prepare output path
            if output_path is None:
                output_path = "temp_output.wav"
                return_bytes = True
            else:
                output_path = Path(output_path)
                if use_default_output_dir and not output_path.is_absolute():
                    output_path = Path("output") / "kokoro" / output_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                return_bytes = False
            
            # Use provided voice or default
            voice_id = voice or self.voice
            
            # Generate audio using Kokoro pipeline
            # The pipeline returns a generator of (graphemes, phonemes, audio) tuples
            audio_chunks = []
            sample_rate = 24000  # Kokoro default sample rate
            
            for _, _, audio in self._pipeline(text, voice=voice_id, speed=speed):
                audio_chunks.append(audio)
            
            # Concatenate all audio chunks
            import numpy as np
            if audio_chunks:
                full_audio = np.concatenate(audio_chunks)
            else:
                raise RuntimeError("No audio generated")
            
            # Save audio
            sf.write(str(output_path), full_audio, sample_rate)
            
            if return_bytes:
                with open(output_path, "rb") as f:
                    audio_bytes = f.read()
                os.remove(output_path)
                return audio_bytes
            
            return str(output_path)
            
        except Exception as e:
            raise RuntimeError(f"Failed to synthesize speech: {str(e)}")

    def get_supported_languages(self) -> list:
        """Get list of supported language codes"""
        return list(self.SUPPORTED_LANGUAGES.keys())
    
    def get_language_names(self) -> dict:
        """Get dictionary mapping language codes to names"""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def get_available_voices(self) -> dict:
        """Get available Hindi voices"""
        return self.HINDI_VOICES.copy()
    
    def synthesize_batch(self, texts: List[str], output_dir: Union[str, Path],
                        voice: Optional[str] = None,
                        speed: float = 1.0,
                        **kwargs) -> List[str]:
        """
        Synthesize multiple texts in batch
        
        Args:
            texts: List of texts to synthesize
            output_dir: Directory to save output files
            voice: Voice ID (optional)
            speed: Speech speed multiplier
            **kwargs: Additional parameters
            
        Returns:
            List of paths to generated audio files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_paths = []
        for i, text in enumerate(texts):
            output_path = output_dir / f"output_{i+1:04d}.wav"
            result = self.synthesize(
                text=text,
                output_path=output_path,
                voice=voice,
                speed=speed,
                use_default_output_dir=False,
                **kwargs
            )
            output_paths.append(result)
        
        return output_paths
