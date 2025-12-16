"""
TTS Playground - A reusable Python module for Text-to-Speech libraries
Supporting multiple TTS engines with easy-to-use interfaces
"""

from tts_playground.base import TTSBase
from tts_playground.factory import get_tts_engine

__version__ = "0.1.0"
__all__ = ["TTSBase", "get_tts_engine"]

