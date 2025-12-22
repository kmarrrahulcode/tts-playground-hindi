"""
Kokoro TTS Implementation
"""

def __getattr__(name):
    if name == "KokoroTTS":
        from tts_playground.kokoro.kokoro_tts import KokoroTTS
        return KokoroTTS
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["KokoroTTS"]
