"""
Example usage of XTTS-Hindi TTS engine
"""

import os
from pathlib import Path
from tts_playground import get_tts_engine

# Ensure HF_TOKEN is set
if not os.getenv("HF_TOKEN"):
    print("Warning: HF_TOKEN environment variable not set!")


def example_basic_usage():
    """Basic usage example"""
    print("=" * 50)
    print("Example 1: Basic TTS Synthesis")
    print("=" * 50)
    
    # Create TTS engine
    tts = get_tts_engine("xtts-hindi", device="cpu")
    
    # Initialize (this will download the model on first run)
    print("\nInitializing model...")
    tts.initialize()
    
    # Synthesize speech
    hindi_text = "नमस्ते, यह एक टेक्स्ट टू स्पीच उदाहरण है।"
    output_path = "output_basic.wav"
    
    print(f"\nSynthesizing: {hindi_text}")
    result = tts.synthesize(
        text=hindi_text,
        output_path=output_path,
        language="hi"
    )
    
    print(f"Audio saved to: {result}")


def example_context_manager():
    """Example using context manager"""
    print("\n" + "=" * 50)
    print("Example 2: Using Context Manager")
    print("=" * 50)
    
    hindi_text = "आज का दिन बहुत सुंदर है।"
    
    with get_tts_engine("xtts-hindi", device="cpu") as tts:
        result = tts.synthesize(
            text=hindi_text,
            output_path="output_context.wav",
            language="hi"
        )
        print(f"Audio saved to: {result}")


def example_batch_synthesis():
    """Example of batch synthesis"""
    print("\n" + "=" * 50)
    print("Example 3: Batch Synthesis")
    print("=" * 50)
    
    hindi_texts = [
        "पहला वाक्य।",
        "दूसरा वाक्य।",
        "तीसरा वाक्य।"
    ]
    
    tts = get_tts_engine("xtts-hindi", device="cpu")
    tts.initialize()
    
    output_dir = Path("batch_output")
    output_paths = tts.synthesize_batch(
        texts=hindi_texts,
        output_dir=output_dir,
        language="hi"
    )
    
    print(f"\nGenerated {len(output_paths)} audio files:")
    for path in output_paths:
        print(f"  - {path}")


def example_voice_cloning():
    """Example of voice cloning with custom voice file"""
    print("\n" + "=" * 50)
    print("Example 4: Voice Cloning with Custom Voice")
    print("=" * 50)
    
    # Path to your recorded voice file
    # Supported formats: .wav, .mp3, .flac, .m4a
    # Recommended: .wav format, mono or stereo, 16kHz or higher sample rate
    # Duration: 3-10 seconds is ideal (longer is OK, shorter may not work well)
    
    #speaker_wav = "my_voice.wav"
    speaker_wav = "my_voice_ankit.wav"
    
    if not Path(speaker_wav).exists():
        print(f"\n⚠️  Voice file not found: {speaker_wav}")
        print("\nTo use voice cloning:")
        print("1. Record your voice saying a few sentences in Hindi")
        print("2. Save it as a .wav file (or .mp3, .flac)")
        print("3. Update the 'speaker_wav' variable above with your file path")
        print("4. Run this example again")
        print("\nRecommended recording settings:")
        print("  - Format: WAV (uncompressed)")
        print("  - Sample rate: 22050 Hz or higher")
        print("  - Channels: Mono or Stereo")
        print("  - Duration: 3-10 seconds")
        return
    
    tts = get_tts_engine("xtts-hindi", device="cpu")
    tts.initialize()
    
    hindi_text = "क्या प्रेम कर्तव्य से बड़ा है? कच और देवयानी की यह कथा हमें धर्म और त्याग का सही अर्थ सिखाती है। प्राचीन काल की बात है, जब देवताओं और असुरों के बीच भीषण संग्राम चल रहा था। असुरों के गुरु शुक्राचार्य के पास 'संजीवनी विद्या' थी, जिससे वे मृत असुरों को पुनर्जीवित कर देते थे।"
    output_path = "output_my_voice.wav"
    
    print(f"\nUsing voice file: {speaker_wav}")
    print(f"Synthesizing: {hindi_text}")
    
    result = tts.synthesize(
        text=hindi_text,
        output_path=output_path,
        speaker_wav=speaker_wav,  # Your voice file
        language="hi"
    )
    
    print(f"Audio saved to: {result}")
    print("The output should sound like your voice!")


def example_direct_import():
    """Example using direct import"""
    print("\n" + "=" * 50)
    print("Example 5: Direct Import")
    print("=" * 50)
    
    from tts_playground.xtts_hindi import XTTSHindi
    
    tts = XTTSHindi(device="cpu")
    tts.initialize()
    
    hindi_text = "यह सीधे आयात का उदाहरण है।"
    result = tts.synthesize(
        text=hindi_text,
        output_path="output_direct.wav",
        language="hi"
    )
    
    print(f"Audio saved to: {result}")
    print(f"Supported languages: {tts.get_supported_languages()}")


if __name__ == "__main__":
    print("TTS Playground - XTTS-Hindi Examples")
    print("=" * 50)
    
    try:
        # Run examples
        #example_basic_usage()
        #example_context_manager()
        #example_batch_synthesis()
        example_voice_cloning()  # Voice cloning with custom voice
        #example_direct_import()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()

