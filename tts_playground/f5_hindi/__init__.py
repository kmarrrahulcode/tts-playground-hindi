"""
F5-Hindi TTS Implementation
"""

def __getattr__(name):
    if name == "F5HindiTTS":
        from tts_playground.f5_hindi.f5_hindi import F5HindiTTS
        return F5HindiTTS
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["F5HindiTTS"]
