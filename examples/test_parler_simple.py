"""
Test Indic Parler TTS with simple descriptions
Based on HuggingFace model card examples
"""

from tts_playground import get_tts_engine

tts = get_tts_engine("indic-parler", device="cpu")
tts.initialize()

# Simple test with minimal description
tests = [
    # Try very simple descriptions
    ("नमस्ते", "A female speaker.", "test_simple1.wav"),
    ("नमस्ते, आप कैसे हैं?", "A male speaker with a calm voice.", "test_simple2.wav"),
    # Try without description (use default)
    ("यह एक परीक्षण है।", None, "test_default.wav"),
]

for text, desc, filename in tests:
    print(f"\nText: {text}")
    print(f"Description: {desc}")
    result = tts.synthesize(text=text, output_path=filename, description=desc)
    print(f"Saved: {result}")
