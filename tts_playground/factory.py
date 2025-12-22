"""
Factory for creating TTS engine instances
"""

from tts_playground.base import TTSBase


def _get_xtts_hindi():
    """Lazy import for XTTSHindi to avoid TTS dependency when not needed"""
    try:
        from tts_playground.xtts_hindi import XTTSHindi
        return XTTSHindi
    except ImportError as e:
        raise ImportError(
            "XTTSHindi requires the TTS library. Install it with: pip install TTS>=0.22.0"
        ) from e


def _get_indic_parler():
    """Lazy import for IndicParlerTTS"""
    try:
        from tts_playground.indic_parler import IndicParlerTTS
        return IndicParlerTTS
    except ImportError as e:
        raise ImportError(
            "IndicParlerTTS requires parler-tts. Install with: pip install parler-tts==0.2.3"
        ) from e


def _get_kokoro():
    """Lazy import for KokoroTTS"""
    try:
        from tts_playground.kokoro import KokoroTTS
        return KokoroTTS
    except ImportError as e:
        raise ImportError(
            "KokoroTTS requires kokoro. Install with: pip install kokoro misaki[hi]"
        ) from e


def _get_f5_hindi():
    """Lazy import for F5HindiTTS"""
    try:
        from tts_playground.f5_hindi import F5HindiTTS
        return F5HindiTTS
    except ImportError as e:
        raise ImportError(
            "F5HindiTTS requires f5-tts. Install with: pip install f5-tts"
        ) from e


# Registry of available TTS engines (using lazy loaders)
TTS_ENGINES = {
    "xtts-hindi": _get_xtts_hindi,
    "xtts_hindi": _get_xtts_hindi,
    "indic-parler": _get_indic_parler,
    "indic_parler": _get_indic_parler,
    "kokoro": _get_kokoro,
    "kokoro-hindi": _get_kokoro,
    "f5-hindi": _get_f5_hindi,
    "f5_hindi": _get_f5_hindi,
}


def get_tts_engine(engine_name: str, **kwargs) -> TTSBase:
    """
    Factory function to create TTS engine instances
    
    Args:
        engine_name: Name of the TTS engine ('xtts-hindi' or 'indic-parler')
        **kwargs: Additional arguments to pass to the engine constructor
        
    Returns:
        Initialized TTS engine instance
    """
    engine_name = engine_name.lower().strip()
    
    if engine_name not in TTS_ENGINES:
        available = ", ".join(TTS_ENGINES.keys())
        raise ValueError(
            f"Unknown TTS engine: {engine_name}. Available engines: {available}"
        )
    
    engine_loader = TTS_ENGINES[engine_name]
    engine_class = engine_loader()
    return engine_class(**kwargs)


def list_available_engines() -> list:
    """Get list of available TTS engine names"""
    return list(TTS_ENGINES.keys())
