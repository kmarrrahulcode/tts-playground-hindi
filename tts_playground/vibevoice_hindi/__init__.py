"""
VibeVoice Hindi TTS Module
High-quality Hindi TTS with voice cloning and multi-speaker support
"""

def __getattr__(name):
    if name == "VibeVoiceHindiTTS":
        from tts_playground.vibevoice_hindi.vibevoice_hindi import VibeVoiceHindiTTS
        return VibeVoiceHindiTTS
    raise AttributeError(f"module {__name__!r} has no attribute {name!r}")

__all__ = ["VibeVoiceHindiTTS"]
