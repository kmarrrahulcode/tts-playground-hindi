"""
Indic Parler TTS Implementation
Text-to-speech for 22 Indian languages using ai4bharat/indic-parler-tts
"""

import os
import torch
import soundfile as sf
from pathlib import Path
from typing import Optional, Union, List

from tts_playground.base import TTSBase


class IndicParlerTTS(TTSBase):
    """
    Indic Parler TTS Engine
    
    Model: ai4bharat/indic-parler-tts
    Supports: 22 Indian languages
    Features: Text-based voice description control
    """
    
    # Supported languages with their codes
    SUPPORTED_LANGUAGES = {
        "as": "Assamese",
        "bn": "Bengali", 
        "brx": "Bodo",
        "doi": "Dogri",
        "en": "English",
        "gom": "Konkani",
        "gu": "Gujarati",
        "hi": "Hindi",
        "kn": "Kannada",
        "ks": "Kashmiri",
        "mai": "Maithili",
        "ml": "Malayalam",
        "mni": "Manipuri",
        "mr": "Marathi",
        "ne": "Nepali",
        "or": "Odia",
        "pa": "Punjabi",
        "sa": "Sanskrit",
        "sat": "Santali",
        "sd": "Sindhi",
        "ta": "Tamil",
        "te": "Telugu",
    }

    # Example voice descriptions
    VOICE_DESCRIPTIONS = {
        "male_calm": "A male speaker with a calm and clear voice.",
        "female_calm": "A female speaker with a calm and clear voice.",
        "male_expressive": "A male speaker with an expressive and energetic voice.",
        "female_expressive": "A female speaker with an expressive and energetic voice.",
    }
    
    def __init__(self, model_name: str = "ai4bharat/indic-parler-tts",
                 device: str = "cpu", hf_token: Optional[str] = None):
        """
        Initialize Indic Parler TTS engine
        
        Args:
            model_name: HuggingFace model name
            device: Device to run on ('cpu' or 'cuda')
            hf_token: HuggingFace token for gated model access (or set HF_TOKEN env var)
        """
        super().__init__(model_name, device)
        self.hf_token = hf_token or os.getenv("HF_TOKEN")
        
        if device == "cpu":
            self.torch_device = torch.device("cpu")
        else:
            self.torch_device = torch.device("cuda" if torch.cuda.is_available() else "cpu")
        
        self._tokenizer = None
        self.default_description = "A female speaker with a calm and clear voice."
    
    def initialize(self):
        """Initialize the Indic Parler TTS model"""
        if self._initialized:
            return
        
        try:
            print(f"Loading Indic Parler TTS model: {self.model_name}")
            print(f"Device: {self.torch_device}")
            
            from parler_tts import ParlerTTSForConditionalGeneration
            from transformers import AutoTokenizer
            
            self._model = ParlerTTSForConditionalGeneration.from_pretrained(
                self.model_name,
                token=self.hf_token
            ).to(self.torch_device)
            
            self._tokenizer = AutoTokenizer.from_pretrained(
                self.model_name,
                token=self.hf_token
            )
            
            self._initialized = True
            print("Indic Parler TTS model loaded successfully!")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Indic Parler TTS: {str(e)}")

    def synthesize(self, text: str, output_path: Optional[Union[str, Path]] = None,
                   description: Optional[str] = None,
                   language: Optional[str] = None,
                   use_default_output_dir: bool = True,
                   **kwargs) -> Union[bytes, str]:
        """
        Synthesize speech from text
        
        Args:
            text: Text to convert to speech
            output_path: Optional path to save audio file (if None, returns bytes)
            description: Voice description (e.g., "A female speaker with a calm voice.")
                        Use get_voice_descriptions() for examples.
            language: Language code (e.g., 'hi' for Hindi). Optional.
            use_default_output_dir: Use output/indic_parler/ folder structure
            **kwargs: Additional generation parameters
            
        Returns:
            Path to saved file if output_path provided, else audio bytes
        """
        if not self._initialized:
            self.initialize()
        
        try:
            # Prepare output path
            if output_path is None:
                output_path = "temp_output.wav"
                return_bytes = True
            else:
                output_path = Path(output_path)
                if use_default_output_dir and not output_path.is_absolute():
                    output_path = Path("output") / "indic_parler" / output_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                return_bytes = False
            
            # Use provided description or default
            voice_description = description or self.default_description
            
            # Tokenize description with attention mask
            description_tokens = self._tokenizer(
                voice_description, 
                return_tensors="pt",
                padding=True
            )
            input_ids = description_tokens.input_ids.to(self.torch_device)
            attention_mask = description_tokens.attention_mask.to(self.torch_device)
            
            # Tokenize text prompt
            prompt_tokens = self._tokenizer(
                text, 
                return_tensors="pt",
                padding=True
            )
            prompt_input_ids = prompt_tokens.input_ids.to(self.torch_device)
            
            # Generate audio with attention mask for description
            generation = self._model.generate(
                input_ids=input_ids,
                attention_mask=attention_mask,
                prompt_input_ids=prompt_input_ids,
                **kwargs
            )
            
            # Get audio array and sample rate
            audio_array = generation.cpu().numpy().squeeze()
            sample_rate = self._model.config.sampling_rate
            
            # Save audio
            sf.write(str(output_path), audio_array, sample_rate)
            
            if return_bytes:
                with open(output_path, "rb") as f:
                    audio_bytes = f.read()
                os.remove(output_path)
                return audio_bytes
            
            return str(output_path)
            
        except Exception as e:
            raise RuntimeError(f"Failed to synthesize speech: {str(e)}")

    def get_supported_languages(self) -> list:
        """Get list of supported language codes"""
        return list(self.SUPPORTED_LANGUAGES.keys())
    
    def get_language_names(self) -> dict:
        """Get dictionary mapping language codes to names"""
        return self.SUPPORTED_LANGUAGES.copy()
    
    def get_voice_descriptions(self) -> dict:
        """Get example voice descriptions"""
        return self.VOICE_DESCRIPTIONS.copy()
    
    def synthesize_batch(self, texts: List[str], output_dir: Union[str, Path],
                        description: Optional[str] = None,
                        **kwargs) -> List[str]:
        """
        Synthesize multiple texts in batch
        
        Args:
            texts: List of texts to synthesize
            output_dir: Directory to save output files
            description: Voice description (optional)
            **kwargs: Additional parameters
            
        Returns:
            List of paths to generated audio files
        """
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        output_paths = []
        for i, text in enumerate(texts):
            output_path = output_dir / f"output_{i+1:04d}.wav"
            result = self.synthesize(
                text=text,
                output_path=output_path,
                description=description,
                use_default_output_dir=False,
                **kwargs
            )
            output_paths.append(result)
        
        return output_paths
