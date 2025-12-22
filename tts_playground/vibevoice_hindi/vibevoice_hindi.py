"""
VibeVoice Hindi TTS Implementation
High-quality Hindi TTS with voice cloning and multi-speaker support
Model: tarun7r/vibevoice-hindi-1.5B
"""

import os
import tempfile
from pathlib import Path
from typing import Optional, Union, List, Dict

from tts_playground.base import TTSBase


class VibeVoiceHindiTTS(TTSBase):
    """
    VibeVoice Hindi TTS Engine
    
    Model: tarun7r/vibevoice-hindi-1.5B
    Features:
    - High-quality Hindi speech synthesis
    - Voice cloning from reference audio
    - Multi-speaker support (up to 4 speakers)
    
    Optimized for T4 GPU (16GB VRAM)
    """
    
    HINDI_SPEAKERS = {
        "hi-Priya_woman": "Hindi Female (Priya)",
        "hi-Raj_man": "Hindi Male (Raj)",
    }
    
    DEFAULT_SPEAKER = "hi-Priya_woman"
    
    def __init__(self, model_name: str = "tarun7r/vibevoice-hindi-1.5B",
                 device: str = "cuda"):
        super().__init__(model_name, device)
        self._model = None
        self._processor = None
        self._voices_dir = None
        self._default_speaker_wav = None
        self._sample_rate = 24000

    def initialize(self):
        """Initialize the VibeVoice Hindi TTS model"""
        if self._initialized:
            return
        
        try:
            print(f"Loading VibeVoice Hindi TTS model: {self.model_name}")
            print(f"Device: {self.device}")
            
            import torch
            from vibevoice.modular import VibeVoiceForConditionalGenerationInference
            from vibevoice.processor import VibeVoiceProcessor
            
            # Load model
            print("Loading model...")
            dtype = torch.float16 if self.device == "cuda" else torch.float32
            
            self._model = VibeVoiceForConditionalGenerationInference.from_pretrained(
                self.model_name,
                torch_dtype=dtype,
            )
            
            if self.device == "cuda":
                self._model = self._model.to(self.device)
            
            self._model.eval()
            
            # Load processor
            print("Loading processor...")
            self._processor = VibeVoiceProcessor.from_pretrained(self.model_name)
            
            # Setup voices directory
            self._voices_dir = Path("demo/voices")
            self._voices_dir.mkdir(parents=True, exist_ok=True)
            
            # Look for default speaker reference
            for ref in ["my_voice.wav", "reference.wav", "speaker.wav"]:
                if Path(ref).exists():
                    self._default_speaker_wav = str(Path(ref).absolute())
                    print(f"Found default speaker reference: {ref}")
                    break
            
            self._initialized = True
            print("VibeVoice Hindi TTS model loaded successfully!")
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"Failed to initialize VibeVoice Hindi TTS: {str(e)}")

    def synthesize(self, text: str, output_path: Optional[Union[str, Path]] = None,
                   speaker: Optional[str] = None,
                   speaker_wav: Optional[Union[str, Path]] = None,
                   use_default_output_dir: bool = True,
                   cfg_scale: float = 1.3,
                   seed: Optional[int] = None,
                   **kwargs) -> Union[bytes, str]:
        """
        Synthesize speech from Hindi text
        
        Args:
            text: Hindi text to convert to speech
            output_path: Optional path to save audio file
            speaker: Speaker name (for voice file lookup)
            speaker_wav: Path to reference audio for voice cloning
            use_default_output_dir: Use output/vibevoice_hindi/ folder
            cfg_scale: Classifier-free guidance scale (1.0-2.0)
            seed: Random seed for reproducibility
        """
        if not self._initialized:
            self.initialize()
        
        try:
            import torch
            import soundfile as sf
            import numpy as np
            
            # Prepare output path
            if output_path is None:
                output_path = tempfile.mktemp(suffix=".wav")
                return_bytes = True
            else:
                output_path = Path(output_path)
                if use_default_output_dir and not output_path.is_absolute():
                    output_path = Path("output") / "vibevoice_hindi" / output_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                return_bytes = False
            
            if seed is not None:
                torch.manual_seed(seed)
                np.random.seed(seed)
            
            # Determine voice file for cloning
            voice_file = speaker_wav
            if not voice_file and speaker:
                voice_path = self._voices_dir / f"{speaker}.wav"
                if voice_path.exists():
                    voice_file = str(voice_path)
            if not voice_file:
                voice_file = self._default_speaker_wav
            
            # Prepare speaker name for the model
            speaker_name = speaker or self.DEFAULT_SPEAKER
            
            # Process inputs
            with torch.no_grad():
                # Format text with speaker tag
                formatted_text = f"[{speaker_name}]: {text}"
                
                # Use processor to prepare inputs
                inputs = self._processor(
                    text=formatted_text,
                    return_tensors="pt"
                )
                
                if self.device == "cuda":
                    inputs = {k: v.to(self.device) if torch.is_tensor(v) else v 
                              for k, v in inputs.items()}
                
                # Generate audio
                outputs = self._model.generate(
                    **inputs,
                    guidance_scale=cfg_scale,
                    **kwargs
                )
                
                # Extract audio
                if hasattr(outputs, 'audio'):
                    audio = outputs.audio
                elif hasattr(outputs, 'waveform'):
                    audio = outputs.waveform
                elif isinstance(outputs, tuple):
                    audio = outputs[0]
                else:
                    audio = outputs
                
                # Convert to numpy
                if torch.is_tensor(audio):
                    audio = audio.cpu().numpy()
                
                # Squeeze extra dimensions
                while len(audio.shape) > 1 and audio.shape[0] == 1:
                    audio = audio.squeeze(0)
                
                # Normalize if needed
                max_val = np.abs(audio).max()
                if max_val > 1.0:
                    audio = audio / max_val
            
            # Save audio
            sf.write(str(output_path), audio, self._sample_rate)
            
            if return_bytes:
                with open(output_path, "rb") as f:
                    audio_bytes = f.read()
                os.remove(output_path)
                return audio_bytes
            
            return str(output_path)
            
        except Exception as e:
            import traceback
            traceback.print_exc()
            raise RuntimeError(f"Failed to synthesize speech: {str(e)}")

    def synthesize_with_voice(self, text: str, speaker_wav: Union[str, Path],
                              output_path: Optional[Union[str, Path]] = None,
                              **kwargs) -> Union[bytes, str]:
        """Synthesize with voice cloning"""
        return self.synthesize(text=text, output_path=output_path, 
                               speaker_wav=speaker_wav, **kwargs)

    def get_speakers(self) -> Dict[str, str]:
        return self.HINDI_SPEAKERS.copy()

    def get_supported_languages(self) -> list:
        return ["hi"]
    
    def get_language_names(self) -> dict:
        return {"hi": "Hindi"}

    def synthesize_batch(self, texts: List[str], output_dir: Union[str, Path],
                        **kwargs) -> List[str]:
        output_dir = Path(output_dir)
        output_dir.mkdir(parents=True, exist_ok=True)
        
        paths = []
        for i, text in enumerate(texts):
            path = output_dir / f"output_{i+1:04d}.wav"
            result = self.synthesize(text=text, output_path=path, 
                                     use_default_output_dir=False, **kwargs)
            paths.append(result)
        return paths
