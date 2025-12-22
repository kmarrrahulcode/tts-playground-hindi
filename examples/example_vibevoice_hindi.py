"""
Example: VibeVoice Hindi TTS
Demonstrates high-quality Hindi TTS with voice cloning and multi-speaker support

Model: tarun7r/vibevoice-hindi-1.5B
Features:
- Built-in Hindi speakers
- Voice cloning from reference audio
- Multi-speaker conversations
- Long-form audio generation

Optimized for T4 GPU (Colab)
"""

from tts_playground import get_tts_engine


def example_basic_synthesis():
    """Basic Hindi TTS with default speaker"""
    print("\n" + "="*60)
    print("Example 1: Basic Hindi Synthesis")
    print("="*60)
    
    # Initialize VibeVoice Hindi (uses CUDA by default)
    tts = get_tts_engine("vibevoice-hindi", device="cuda")
    tts.initialize()
    
    # Hindi text
    text = "नमस्ते, मैं विबवॉइस हिंदी हूं। मैं उच्च गुणवत्ता वाली हिंदी वाणी उत्पन्न कर सकता हूं।"
    
    # Synthesize with default speaker (hi-Priya_woman)
    output_path = tts.synthesize(
        text=text,
        output_path="vibevoice_basic.wav"
    )
    
    print(f"Generated: {output_path}")
    return output_path


def example_speaker_selection():
    """Using different built-in Hindi speakers"""
    print("\n" + "="*60)
    print("Example 2: Different Speakers")
    print("="*60)
    
    tts = get_tts_engine("vibevoice-hindi", device="cuda")
    tts.initialize()
    
    # Show available speakers
    speakers = tts.get_speakers()
    print("Available speakers:")
    for speaker_id, description in speakers.items():
        print(f"  - {speaker_id}: {description}")
    
    text = "आज का मौसम बहुत अच्छा है। आइए बाहर घूमने चलते हैं।"
    
    # Generate with different speakers
    outputs = []
    for speaker in ["hi-Priya_woman", "hi-Raj_man"]:
        output_path = tts.synthesize(
            text=text,
            speaker=speaker,
            output_path=f"vibevoice_{speaker}.wav"
        )
        print(f"Generated with {speaker}: {output_path}")
        outputs.append(output_path)
    
    return outputs


def example_voice_cloning():
    """Voice cloning from reference audio"""
    print("\n" + "="*60)
    print("Example 3: Voice Cloning")
    print("="*60)
    
    tts = get_tts_engine("vibevoice-hindi", device="cuda")
    tts.initialize()
    
    # Reference audio file (your voice sample)
    reference_audio = "my_voice.wav"  # Place your voice file here
    
    text = "यह मेरी आवाज़ की क्लोनिंग है। विबवॉइस बहुत अच्छी तरह से आवाज़ की नकल कर सकता है।"
    
    output_path = tts.synthesize_with_voice(
        text=text,
        speaker_wav=reference_audio,
        output_path="vibevoice_cloned.wav",
        cfg_scale=1.3,  # Higher = more faithful to reference
        seed=42  # For reproducibility
    )
    
    print(f"Generated with voice cloning: {output_path}")
    return output_path


def example_conversation():
    """Multi-speaker conversation"""
    print("\n" + "="*60)
    print("Example 4: Multi-Speaker Conversation")
    print("="*60)
    
    tts = get_tts_engine("vibevoice-hindi", device="cuda")
    tts.initialize()
    
    # Define a conversation
    dialogue = [
        {"speaker": "hi-Priya_woman", "text": "नमस्ते राज, कैसे हो आप?"},
        {"speaker": "hi-Raj_man", "text": "नमस्ते प्रिया, मैं ठीक हूं। आप कैसी हैं?"},
        {"speaker": "hi-Priya_woman", "text": "मैं भी अच्छी हूं। आज का दिन बहुत सुहाना है।"},
        {"speaker": "hi-Raj_man", "text": "हां, बिल्कुल। चलो पार्क में चलते हैं।"},
    ]
    
    output_path = tts.synthesize_conversation(
        dialogue=dialogue,
        output_path="vibevoice_conversation.wav",
        cfg_scale=1.3
    )
    
    print(f"Generated conversation: {output_path}")
    return output_path


def example_batch_synthesis():
    """Batch synthesis of multiple texts"""
    print("\n" + "="*60)
    print("Example 5: Batch Synthesis")
    print("="*60)
    
    tts = get_tts_engine("vibevoice-hindi", device="cuda")
    tts.initialize()
    
    texts = [
        "पहला वाक्य: भारत एक महान देश है।",
        "दूसरा वाक्य: हिंदी हमारी राष्ट्रभाषा है।",
        "तीसरा वाक्य: विज्ञान और तकनीक में भारत आगे बढ़ रहा है।",
    ]
    
    output_paths = tts.synthesize_batch(
        texts=texts,
        output_dir="output/vibevoice_hindi/batch",
        speaker="hi-Priya_woman"
    )
    
    print(f"Generated {len(output_paths)} files:")
    for path in output_paths:
        print(f"  - {path}")
    
    return output_paths


def example_custom_voice():
    """Add and use a custom voice"""
    print("\n" + "="*60)
    print("Example 6: Custom Voice")
    print("="*60)
    
    tts = get_tts_engine("vibevoice-hindi", device="cuda")
    tts.initialize()
    
    # Add a custom voice from your audio file
    custom_speaker_id = tts.add_custom_voice(
        voice_name="my_custom_voice",
        voice_wav="my_voice.wav"
    )
    
    text = "यह मेरी कस्टम आवाज़ है जो मैंने जोड़ी है।"
    
    output_path = tts.synthesize(
        text=text,
        speaker=custom_speaker_id,
        output_path="vibevoice_custom_voice.wav"
    )
    
    print(f"Generated with custom voice: {output_path}")
    return output_path


if __name__ == "__main__":
    print("VibeVoice Hindi TTS Examples")
    print("Model: tarun7r/vibevoice-hindi-1.5B")
    print("="*60)
    
    # Run examples
    try:
        # Basic synthesis (always works)
        example_basic_synthesis()
        
        # Speaker selection
        example_speaker_selection()
        
        # Voice cloning (requires my_voice.wav)
        import os
        if os.path.exists("my_voice.wav"):
            example_voice_cloning()
            example_custom_voice()
        else:
            print("\nSkipping voice cloning examples (my_voice.wav not found)")
        
        # Multi-speaker conversation
        example_conversation()
        
        # Batch synthesis
        example_batch_synthesis()
        
        print("\n" + "="*60)
        print("All examples completed!")
        print("Check output/vibevoice_hindi/ for generated files")
        print("="*60)
        
    except Exception as e:
        print(f"\nError: {e}")
        print("Make sure you have installed: pip install -r requirements-vibevoice.txt")
