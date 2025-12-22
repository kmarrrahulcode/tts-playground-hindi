"""
Indic Parler TTS Implementation
"""

def __getattr__(name):
    if name == "IndicParlerTTS":
        from tts_playground.indic_parler.indic_parler import IndicParlerTTS
        return IndicParlerTTS
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["IndicParlerTTS"]
