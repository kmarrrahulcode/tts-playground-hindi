"""
Example: F5-Hindi TTS (Voice Cloning)
Demonstrates Hindi text-to-speech with voice cloning using F5-TTS

Usage:
    1. Activate venv-f5hindi: venv-f5hindi\Scripts\activate
    2. Place a reference audio file (e.g., my_voice.wav) in the workspace
    3. Run: python examples/example_f5_hindi.py
"""

from pathlib import Path
from tts_playground import get_tts_engine


def main():
    # Check for reference audio
    ref_audio = None
    for ref_file in ["my_voice.wav", "reference.wav", "speaker.wav"]:
        if Path(ref_file).exists():
            ref_audio = ref_file
            break
    
    if not ref_audio:
        print("ERROR: No reference audio file found!")
        print("Please place a reference audio file (my_voice.wav) in the workspace.")
        print("F5-Hindi is a voice cloning model - it needs a voice sample to clone.")
        return
    
    print(f"Using reference audio: {ref_audio}")
    
    # Initialize F5-Hindi TTS engine
    print("\nInitializing F5-Hindi TTS...")
    tts = get_tts_engine("f5-hindi", device="cpu")
    
    # Hindi text samples
    hindi_texts = [
        "नमस्ते, आप कैसे हैं?",
        "आज मौसम बहुत अच्छा है।",
        "भारत एक महान देश है।",
    ]
    
    # Optional: transcript of reference audio (improves quality)
    ref_text = ""  # Add transcript if available
    
    # Generate speech for each text
    for i, text in enumerate(hindi_texts):
        print(f"\nGenerating audio for: {text}")
        output_path = tts.synthesize(
            text=text,
            output_path=f"f5_hindi_output_{i+1}.wav",
            speaker_wav=ref_audio,
            ref_text=ref_text
        )
        print(f"Saved to: {output_path}")
    
    print("\nDone! Check the output/f5_hindi/ folder for generated audio files.")


if __name__ == "__main__":
    main()
