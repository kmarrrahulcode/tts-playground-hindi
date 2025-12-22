"""
Example: Indic Parler TTS
Demonstrates text-to-speech for Indian languages using ai4bharat/indic-parler-tts
"""

from tts_playground import get_tts_engine


def main():
    # Create TTS engine
    tts = get_tts_engine("indic-parler", device="cpu")
    
    # Initialize model (downloads on first run)
    tts.initialize()
    
    # Print supported languages
    print("Supported languages:")
    for code, name in tts.get_language_names().items():
        print(f"  {code}: {name}")
    
    # Voice descriptions - be specific about speaking style
    # The model responds well to detailed descriptions
    descriptions = {
        "hindi_female": "A clear and natural female voice speaking Hindi with proper pronunciation and moderate pace.",
        "hindi_male": "A clear male voice speaking Hindi in a calm, natural tone.",
        "tamil_female": "A female speaker delivering Tamil speech clearly and naturally.",
    }
    
    # Example texts
    examples = [
        ("hi", "नमस्ते, आप कैसे हैं?", "hindi_greeting.wav", descriptions["hindi_female"]),
        ("hi", "आज मौसम बहुत अच्छा है।", "hindi_weather.wav", descriptions["hindi_male"]),
        ("ta", "வணக்கம், நீங்கள் எப்படி இருக்கிறீர்கள்?", "tamil_greeting.wav", descriptions["tamil_female"]),
    ]
    
    # Generate audio for each example
    for lang, text, filename, desc in examples:
        print(f"\nGenerating {lang}: {text[:30]}...")
        
        output = tts.synthesize(
            text=text,
            output_path=filename,
            description=desc,
        )
        print(f"Saved to: {output}")


if __name__ == "__main__":
    main()
