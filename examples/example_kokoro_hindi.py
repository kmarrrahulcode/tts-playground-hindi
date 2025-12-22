"""
Example: Kokoro TTS Hindi
Demonstrates Hindi text-to-speech using Kokoro

Usage:
    1. Activate venv-kokoro: venv-kokoro\Scripts\activate
    2. Run: python examples/example_kokoro_hindi.py
"""

from tts_playground import get_tts_engine


def main():
    # Initialize Kokoro TTS engine
    print("Initializing Kokoro TTS for Hindi...")
    
    # Available Hindi voices:
    # hf_alpha, hf_beta (female), hm_omega, hm_psi (male)
    tts = get_tts_engine("kokoro", device="cpu", voice="hm_psi")
    
    # Print available voices
    print(f"Available Hindi voices: {list(tts.get_available_voices().keys())}")
    
    # Hindi text samples
    hindi_texts = [
        "कथा तब की है जब देवराज इंद्र के अहंकार से क्रुद्ध होकर महादेव ने अपने तीसरे नेत्र की अग्नि को सागर में फेंक दिया था।",
        "मेरा नाम कोकोरो है।",
        "उस प्रलयंकारी अग्नि से सागर के गर्भ में एक बालक का जन्म हुआ। उसका क्रंदन सुनकर धरती कांप उठी। ....वह बालक था—जालंधर।",
    ]
    
    # Generate speech for each text
    for i, text in enumerate(hindi_texts):
        print(f"\nGenerating audio for: {text}")
        output_path = tts.synthesize(
            text=text,
            output_path=f"hindi_output_{i+1}.wav",
            speed=1.0
        )
        print(f"Saved to: {output_path}")
    
    print("\nDone! Check the output/kokoro/ folder for generated audio files.")


if __name__ == "__main__":
    main()
