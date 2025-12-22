"""
XTTS-Hindi TTS Engine
Based on: https://huggingface.co/Abhinay45/XTTS-Hindi-finetuned
"""

def __getattr__(name):
    if name == "XTTSHindi":
        from tts_playground.xtts_hindi.xtts_hindi import XTTSHindi
        return XTTSHindi
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["XTTSHindi"]
