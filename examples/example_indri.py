"""
Example usage of Indri TTS engine
Supports English and Hindi with multiple pre-trained speakers
Note: Indri does NOT support voice cloning - use XTTS-Hindi for that
"""

import os
from pathlib import Path
from tts_playground import get_tts_engine

# Ensure HF_TOKEN is set (optional for Indri, but recommended)
if not os.getenv("HF_TOKEN"):
    print("Note: HF_TOKEN not set. Some models may require it.")


def example_basic_usage():
    """Basic usage example with default speaker"""
    print("=" * 50)
    print("Example 1: Basic TTS Synthesis (Hindi)")
    print("=" * 50)
    
    # Create TTS engine
    tts = get_tts_engine("indri", device="cpu")
    
    # Initialize (this will download the model on first run)
    print("\nInitializing model...")
    tts.initialize()
    
    # Synthesize speech in Hindi
    hindi_text = "नमस्ते, यह इंद्री टीटीएस मॉडल का उदाहरण है।"
    output_path = "output_indri_hindi.wav"
    
    print(f"\nSynthesizing: {hindi_text}")
    result = tts.synthesize(
        text=hindi_text,
        output_path=output_path,
    )
    
    print(f"Audio saved to: {result}")


def example_english_usage():
    """Example with English text"""
    print("\n" + "=" * 50)
    print("Example 2: English TTS")
    print("=" * 50)
    
    tts = get_tts_engine("indri", device="cpu")
    tts.initialize()
    
    english_text = "Hello, this is the Indri TTS model. It supports both English and Hindi."
    result = tts.synthesize(
        text=english_text,
        output_path="output_indri_english.wav",
    )
    
    print(f"Audio saved to: {result}")


def example_code_mixing():
    """Example with code-mixed text (English + Hindi)"""
    print("\n" + "=" * 50)
    print("Example 3: Code-Mixed Text (English + Hindi)")
    print("=" * 50)
    
    tts = get_tts_engine("indri", device="cpu")
    tts.initialize()
    
    # Code-mixed text
    mixed_text = "Hello दोस्तों, future of speech technology mein अपका स्वागत है"
    result = tts.synthesize(
        text=mixed_text,
        output_path="output_indri_mixed.wav",
    )
    
    print(f"Audio saved to: {result}")


def example_different_speakers():
    """Example showing different speakers"""
    print("\n" + "=" * 50)
    print("Example 4: Different Speakers")
    print("=" * 50)
    
    tts = get_tts_engine("indri", device="cpu")
    tts.initialize()
    
    # Show available speakers
    speakers = tts.get_available_speakers()
    print("\nAvailable speakers:")
    for speaker_id, description in list(speakers.items())[:5]:  # Show first 5
        print(f"  {speaker_id}: {description}")
    
    # Use a specific speaker
    text = "नमस्ते, मैं एक अलग आवाज़ में बोल रहा हूं।"
    
    # Try different speakers
    test_speakers = ["[spkr_68]", "[spkr_70]", "[spkr_53]"]
    
    for speaker_id in test_speakers:
        output_path = f"output_indri_{speaker_id.replace('[', '').replace(']', '')}.wav"
        result = tts.synthesize(
            text=text,
            output_path=output_path,
            speaker=speaker_id
        )
        print(f"\n{speaker_id} ({speakers.get(speaker_id, 'Unknown')}):")
        print(f"  Saved to: {result}")


def example_batch_synthesis():
    """Example of batch synthesis"""
    print("\n" + "=" * 50)
    print("Example 5: Batch Synthesis")
    print("=" * 50)
    
    tts = get_tts_engine("indri", device="cpu")
    tts.initialize()
    
    texts = [
        "पहला वाक्य।",
        "दूसरा वाक्य।",
        "तीसरा वाक्य।"
    ]
    
    output_dir = Path("indri_batch_output")
    output_paths = tts.synthesize_batch(
        texts=texts,
        output_dir=output_dir,
    )
    
    print(f"\nGenerated {len(output_paths)} audio files:")
    for path in output_paths:
        print(f"  - {path}")


def example_long_text_synthesis():
    """Example of synthesizing longer text with proper parameters"""
    print("\n" + "=" * 50)
    print("Example 6: Long Text Synthesis")
    print("=" * 50)
    
    tts = get_tts_engine("indri", device="cpu")
    tts.initialize()
    
    # Long Hindi text
    long_text = "क्या प्रेम कर्तव्य से बड़ा है? कच और देवयानी की यह कथा हमें धर्म और त्याग का सही अर्थ सिखाती है। प्राचीन काल की बात है, जब देवताओं और असुरों के बीच भीषण संग्राम चल रहा था।"
    
    print(f"\nText ({len(long_text)} characters):")
    print(f"{long_text}\n")
    
    # For longer text, increase max_new_tokens to avoid truncation
    print("Synthesizing with max_new_tokens=4096 to capture full text...")
    
    result = tts.synthesize(
        text=long_text,
        output_path="output_indri_long.wav",
        speaker="[spkr_68]",  # Hindi book reader
        max_new_tokens=4096,  # Increased for longer text
    )
    
    print(f"✓ Audio saved to: {result}")
    print("\nNote: For very long text, use max_new_tokens=8192 or higher")
    print("      See TRUNCATION_FIX.md for details")


def example_context_manager():
    """Example using context manager"""
    print("\n" + "=" * 50)
    print("Example 7: Using Context Manager")
    print("=" * 50)
    
    text = "यह context manager का उदाहरण है।"
    
    with get_tts_engine("indri", device="cpu") as tts:
        result = tts.synthesize(
            text=text,
            output_path="output_indri_context.wav",
        )
        print(f"Audio saved to: {result}")


if __name__ == "__main__":
    print("TTS Playground - Indri TTS Examples")
    print("=" * 50)
    print("Note: Indri uses pre-trained speakers only")
    print("      For voice cloning, use XTTS-Hindi instead")
    print("=" * 50)
    
    try:
        # Run examples
        example_basic_usage()
        example_english_usage()
        example_code_mixing()
        example_different_speakers()
        example_batch_synthesis()
        example_long_text_synthesis()
        example_context_manager()
        
        print("\n" + "=" * 50)
        print("All examples completed successfully!")
        print("=" * 50)
        
    except Exception as e:
        print(f"\nError: {str(e)}")
        import traceback
        traceback.print_exc()
