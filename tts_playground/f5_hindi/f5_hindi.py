"""
F5-Hindi TTS Implementation
Voice cloning TTS for Hindi using SPRINGLab/F5-Hindi-24KHz
"""

import os
import soundfile as sf
from pathlib import Path
from typing import Optional, Union, List

from tts_playground.base import TTSBase


class F5HindiTTS(TTSBase):
    """
    F5-Hindi TTS Engine (Voice Cloning)
    
    Model: SPRINGLab/F5-Hindi-24KHz
    Features: High-quality voice cloning for Hindi
    Requires: Reference audio file for voice cloning
    """
    
    SUPPORTED_LANGUAGES = {
        "hi": "Hindi",
    }
    
    def __init__(self, model_name: str = "SPRINGLab/F5-Hindi-24KHz",
                 device: str = "cpu"):
        """
        Initialize F5-Hindi TTS engine
        
        Args:
            model_name: HuggingFace model name
            device: Device to run on ('cpu' or 'cuda')
        """
        super().__init__(model_name, device)
        self._tts = None
        self._default_speaker_wav = None

    def initialize(self):
        """Initialize the F5-Hindi TTS model"""
        if self._initialized:
            return
        
        try:
            print(f"Loading F5-Hindi TTS model: {self.model_name}")
            print(f"Device: {self.device}")
            
            from f5_tts.api import F5TTS
            from huggingface_hub import hf_hub_download
            
            # Download the model checkpoint from HuggingFace
            print("Downloading model from HuggingFace...")
            ckpt_path = hf_hub_download(
                repo_id=self.model_name,
                filename="model_2500000.safetensors"
            )
            
            # Download vocab file
            vocab_path = hf_hub_download(
                repo_id=self.model_name,
                filename="vocab.txt"
            )
            
            print(f"Model checkpoint: {ckpt_path}")
            print(f"Vocab file: {vocab_path}")
            
            # SPRINGLab/F5-Hindi-24KHz uses the "small" model config (151M params)
            # This requires F5TTS_Small model type
            # The model has: dim=768, depth=18, heads=12, ff_mult=2
            self._tts = F5TTS(
                model="F5TTS_Small",  # Small model for SPRINGLab Hindi
                ckpt_file=ckpt_path,
                vocab_file=vocab_path,
                device=self.device if self.device != "cpu" else None
            )
            
            # Look for default speaker reference in workspace
            default_refs = ["my_voice.wav", "reference.wav", "speaker.wav"]
            for ref in default_refs:
                if Path(ref).exists():
                    self._default_speaker_wav = str(Path(ref).absolute())
                    print(f"Found default speaker reference: {ref}")
                    break
            
            self._initialized = True
            print("F5-Hindi TTS model loaded successfully!")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize F5-Hindi TTS: {str(e)}")

    def synthesize(self, text: str, output_path: Optional[Union[str, Path]] = None,
                   speaker_wav: Optional[Union[str, Path]] = None,
                   ref_text: Optional[str] = None,
                   use_default_output_dir: bool = True,
                   speed: float = 1.0,
                   **kwargs) -> Union[bytes, str]:
        """
        Synthesize speech from text using voice cloning
        
        Args:
            text: Hindi text to convert to speech
            output_path: Optional path to save audio file (if None, returns bytes)
            speaker_wav: Path to reference speaker audio for voice cloning (required)
            ref_text: Transcript of the reference audio (optional, improves quality)
            use_default_output_dir: Use output/f5_hindi/ folder structure
            speed: Speech speed (default 1.0)
            **kwargs: Additional generation parameters
            
        Returns:
            Path to saved file if output_path provided, else audio bytes
        """
        if not self._initialized:
            self.initialize()
        
        try:
            # Use provided speaker_wav or default
            ref_audio = speaker_wav or self._default_speaker_wav
            if not ref_audio:
                raise ValueError(
                    "F5-Hindi requires a speaker reference audio file (speaker_wav). "
                    "Provide speaker_wav parameter or place 'my_voice.wav' in workspace."
                )
            
            # Prepare output path
            if output_path is None:
                output_path = "temp_output.wav"
                return_bytes = True
            else:
                output_path = Path(output_path)
                if use_default_output_dir and not output_path.is_absolute():
                    output_path = Path("output") / "f5_hindi" / output_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                return_bytes = False
            
            # Generate audio using F5-TTS
            # The infer method saves directly to file via file_wave parameter
            self._tts.infer(
                ref_file=str(ref_audio),
                ref_text=ref_text or "",
                gen_text=text,
                file_wave=str(output_path),
                speed=speed,
                **kwargs
            )
            
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
    
    def synthesize_batch(self, texts: List[str], output_dir: Union[str, Path],
                        speaker_wav: Optional[Union[str, Path]] = None,
                        ref_text: Optional[str] = None,
                        **kwargs) -> List[str]:
        """
        Synthesize multiple texts in batch
        
        Args:
            texts: List of texts to synthesize
            output_dir: Directory to save output files
            speaker_wav: Reference speaker audio (required)
            ref_text: Transcript of reference audio (optional)
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
                speaker_wav=speaker_wav,
                ref_text=ref_text,
                use_default_output_dir=False,
                **kwargs
            )
            output_paths.append(result)
        
        return output_paths
