"""
Voice Cloning Example - Using Your Own Voice
This example shows how to use your own recorded voice for TTS synthesis
"""

import os
from pathlib import Path
from tts_playground import get_tts_engine

# Ensure HF_TOKEN is set
if not os.getenv("HF_TOKEN"):
    print("Warning: HF_TOKEN environment variable not set!")


def clone_voice_with_custom_file():
    """
    Clone voice using your own recorded audio file
    
    Steps:
    1. Record your voice saying a few sentences in Hindi (3-10 seconds)
    2. Save it as a .wav, .mp3, or .flac file
    3. Update the 'your_voice_file' variable below with your file path
    4. Run this script
    """
    
    # ===== CONFIGURATION =====
    # Update this path to your voice recording file
    your_voice_file = "my_voice.wav"  # Change this!
    
    # Text to synthesize in your voice
    hindi_text = "नमस्ते, मैं आपसे बात कर रहा हूं। यह मेरी आवाज़ है।"
    
    # Output file name
    output_file = "output_my_voice.wav"
    # ==========================
    
    # Check if voice file exists
    voice_path = Path(your_voice_file)
    if not voice_path.exists():
        print("=" * 60)
        print("Voice file not found!")
        print("=" * 60)
        print(f"\nExpected file: {voice_path.absolute()}")
        print("\nPlease:")
        print("1. Record your voice (3-10 seconds of Hindi speech)")
        print("2. Save it as a .wav, .mp3, or .flac file")
        print("3. Update 'your_voice_file' variable in this script")
        print("4. Run the script again")
        print("\nRecommended recording settings:")
        print("  - Format: WAV (uncompressed) or MP3")
        print("  - Sample rate: 22050 Hz or higher")
        print("  - Duration: 3-10 seconds")
        print("  - Content: Clear Hindi speech, minimal background noise")
        return
    
    print("=" * 60)
    print("Voice Cloning with Custom Voice File")
    print("=" * 60)
    print(f"\nVoice file: {voice_path.absolute()}")
    print(f"Text to synthesize: {hindi_text}")
    print(f"Output file: {output_file}")
    
    # Create TTS engine
    print("\nInitializing TTS engine...")
    tts = get_tts_engine("xtts-hindi", device="cpu")
    tts.initialize()
    
    # Synthesize speech using your voice
    print("\nSynthesizing speech with your voice...")
    result = tts.synthesize(
        text=hindi_text,
        output_path=output_file,
        speaker_wav=str(voice_path),  # Your voice file
        language="hi"
    )
    
    print(f"\n✓ Success! Audio saved to: {result}")
    print(f"  The output should sound like your voice!")


def clone_voice_multiple_texts():
    """
    Clone voice for multiple texts using the same voice file
    """
    
    your_voice_file = "my_voice.wav"  # Your voice file
    
    texts = [
        "पहला वाक्य मेरी आवाज़ में।",
        "दूसरा वाक्य भी मेरी आवाज़ में है।",
        "तीसरा वाक्य भी मेरी आवाज़ की तरह लगेगा।"
    ]
    
    voice_path = Path(your_voice_file)
    if not voice_path.exists():
        print(f"Voice file not found: {voice_path}")
        print("Please update 'your_voice_file' variable")
        return
    
    print("=" * 60)
    print("Batch Voice Cloning")
    print("=" * 60)
    
    tts = get_tts_engine("xtts-hindi", device="cpu")
    tts.initialize()
    
    output_dir = Path("my_voice_outputs")
    output_dir.mkdir(exist_ok=True)
    
    print(f"\nGenerating {len(texts)} audio files with your voice...")
    
    for i, text in enumerate(texts, 1):
        output_path = output_dir / f"my_voice_{i:02d}.wav"
        print(f"\n[{i}/{len(texts)}] {text}")
        
        result = tts.synthesize(
            text=text,
            output_path=str(output_path),
            speaker_wav=str(voice_path),
            language="hi"
        )
        
        print(f"  ✓ Saved: {result}")
    
    print(f"\n✓ All files saved to: {output_dir}")


if __name__ == "__main__":
    # Run the main voice cloning example
    clone_voice_with_custom_file()
    
    # Uncomment the line below to try batch voice cloning
    # clone_voice_multiple_texts()

