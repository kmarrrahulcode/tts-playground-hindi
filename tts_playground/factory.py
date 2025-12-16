"""
Factory for creating TTS engine instances
"""

from typing import Optional, Dict, Any
from tts_playground.base import TTSBase
from tts_playground.xtts_hindi import XTTSHindi
from tts_playground.indri import IndriTTS


# Registry of available TTS engines
TTS_ENGINES = {
    "xtts-hindi": XTTSHindi,
    "xtts_hindi": XTTSHindi,  # Alternative naming
    "indri": IndriTTS,
    "indri-tts": IndriTTS,  # Alternative naming
}


def get_tts_engine(engine_name: str, **kwargs) -> TTSBase:
    """
    Factory function to create TTS engine instances
    
    Args:
        engine_name: Name of the TTS engine (e.g., 'xtts-hindi')
        **kwargs: Additional arguments to pass to the engine constructor
        
    Returns:
        Initialized TTS engine instance
        
    Example:
        >>> tts = get_tts_engine("xtts-hindi", device="cpu")
        >>> tts.initialize()
        >>> audio = tts.synthesize("नमस्ते", output_path="output.wav")
    """
    engine_name = engine_name.lower().strip()
    
    if engine_name not in TTS_ENGINES:
        available = ", ".join(TTS_ENGINES.keys())
        raise ValueError(
            f"Unknown TTS engine: {engine_name}. "
            f"Available engines: {available}"
        )
    
    engine_class = TTS_ENGINES[engine_name]
    return engine_class(**kwargs)


def list_available_engines() -> list:
    """Get list of available TTS engine names"""
    return list(TTS_ENGINES.keys())

