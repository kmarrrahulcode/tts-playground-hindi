"""Corrected Indri example - using pre-trained speakers only"""
import os
from tts_playground import get_tts_engine

os.environ["HF_TOKEN"] = "<SET HF_TOKEN>"

print("Indri TTS - Corrected Example")
print("=" * 50)
print("Note: Indri does NOT support voice cloning")
print("      It only has 13 pre-trained speakers")
print("=" * 50)

tts = get_tts_engine("indri", device="cpu")
tts.initialize()

# Long Hindi text
long_text = "क्या प्रेम कर्तव्य से बड़ा है? कच और देवयानी की यह कथा हमें धर्म और त्याग का सही अर्थ सिखाती है। प्राचीन काल की बात है, जब देवताओं और असुरों के बीच भीषण संग्राम चल रहा था।"

print(f"\nText ({len(long_text)} characters):")
print(f"{long_text}\n")

# Test with different pre-trained speakers
test_speakers = [
    ("[spkr_68]", "Hindi book reader (male)"),
    ("[spkr_70]", "Hindi motivational speaker (male)"),
    ("[spkr_53]", "Hindi recipe reciter (female)"),
]

for speaker_id, description in test_speakers:
    output_path = f"output_indri_{speaker_id.replace('[', '').replace(']', '')}.wav"
    
    print(f"\nSpeaker: {speaker_id} - {description}")
    
    result = tts.synthesize(
        text=long_text,
        output_path=output_path,
        speaker=speaker_id,
        max_new_tokens=4096  # Increased for longer text
    )
    
    print(f"✓ Saved to: {result}")

print("\n" + "=" * 50)
print("Compare the different speakers!")
print("For voice cloning, use XTTS-Hindi instead.")
print("=" * 50)
