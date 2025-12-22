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
    - Long-form audio generation (~90 min)
    
    Optimized for T4 GPU (16GB VRAM)
    """
    
    # Built-in Hindi speakers
    HINDI_SPEAKERS = {
        "hi-Priya_woman": "Hindi Female (Priya) - Calm, clear voice",
        "hi-Raj_man": "Hindi Male (Raj) - Professional tone",
        "hi-Ananya_woman": "Hindi Female (Ananya) - Expressive voice",
        "hi-Vikram_man": "Hindi Male (Vikram) - Deep, authoritative",
    }
    
    DEFAULT_SPEAKER = "hi-Priya_woman"
    
    def __init__(self, model_name: str = "tarun7r/vibevoice-hindi-1.5B",
                 device: str = "cuda"):
        """
        Initialize VibeVoice Hindi TTS engine
        
        Args:
            model_name: HuggingFace model name
            device: Device to run on ('cpu' or 'cuda')
        """
        super().__init__(model_name, device)
        self._pipeline = None
        self._model = None
        self._voices_dir = None
        self._default_speaker_wav = None

    def initialize(self):
        """Initialize the VibeVoice Hindi TTS model"""
        if self._initialized:
            return
        
        try:
            print(f"Loading VibeVoice Hindi TTS model: {self.model_name}")
            print(f"Device: {self.device}")
            
            import torch
            from vibevoice import VibeVoicePipeline
            
            # Use float16 for T4 GPU memory efficiency
            dtype = torch.float16 if self.device == "cuda" else torch.float32
            
            print("Downloading and loading model from HuggingFace...")
            self._pipeline = VibeVoicePipeline.from_pretrained(
                self.model_name,
                torch_dtype=dtype,
                device_map=self.device if self.device == "cuda" else None
            )
            
            if self.device == "cuda":
                self._pipeline = self._pipeline.to(self.device)
            
            # Setup voices directory
            self._voices_dir = Path("demo/voices")
            self._voices_dir.mkdir(parents=True, exist_ok=True)
            
            # Look for default speaker reference in workspace
            default_refs = ["my_voice.wav", "reference.wav", "speaker.wav"]
            for ref in default_refs:
                if Path(ref).exists():
                    self._default_speaker_wav = str(Path(ref).absolute())
                    print(f"Found default speaker reference: {ref}")
                    break
            
            self._initialized = True
            print("VibeVoice Hindi TTS model loaded successfully!")
            print(f"Available speakers: {list(self.HINDI_SPEAKERS.keys())}")
            
        except ImportError as e:
            raise ImportError(
                "VibeVoice requires the vibevoice library. "
                "Install with: pip install vibevoice @ git+https://github.com/vibevoice-community/VibeVoice.git"
            ) from e
        except Exception as e:
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
            speaker: Speaker ID (e.g., 'hi-Priya_woman') - use get_speakers() for list
            speaker_wav: Path to reference audio for voice cloning (overrides speaker)
            use_default_output_dir: Use output/vibevoice_hindi/ folder structure
            cfg_scale: Classifier-free guidance scale (1.0-2.0, default 1.3)
            seed: Random seed for reproducibility
            **kwargs: Additional generation parameters
            
        Returns:
            Path to saved file if output_path provided, else audio bytes
        """
        if not self._initialized:
            self.initialize()
        
        try:
            import torch
            import soundfile as sf
            
            # Determine speaker/voice to use
            voice_file = None
            speaker_name = speaker or self.DEFAULT_SPEAKER
            
            if speaker_wav:
                # Voice cloning mode
                voice_file = str(speaker_wav)
                speaker_name = "custom_voice"
            elif speaker and speaker in self.HINDI_SPEAKERS:
                # Check if voice file exists
                voice_path = self._voices_dir / f"{speaker}.wav"
                if voice_path.exists():
                    voice_file = str(voice_path)
            elif self._default_speaker_wav:
                voice_file = self._default_speaker_wav
            
            # Prepare output path
            if output_path is None:
                output_path = "temp_output.wav"
                return_bytes = True
            else:
                output_path = Path(output_path)
                if use_default_output_dir and not output_path.is_absolute():
                    output_path = Path("output") / "vibevoice_hindi" / output_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                return_bytes = False
            
            # Set seed if provided
            if seed is not None:
                torch.manual_seed(seed)
            
            # Generate audio
            generation_kwargs = {
                "text": text,
                "speaker_names": [speaker_name],
                "cfg_scale": cfg_scale,
                **kwargs
            }
            
            if voice_file:
                generation_kwargs["voice_file"] = voice_file
            
            audio_output = self._pipeline.generate(**generation_kwargs)
            
            # Save audio
            if hasattr(audio_output, 'audio'):
                audio_data = audio_output.audio
                sample_rate = audio_output.sample_rate
            else:
                audio_data = audio_output
                sample_rate = 24000  # Default sample rate
            
            sf.write(str(output_path), audio_data, sample_rate)
            
            if return_bytes:
                with open(output_path, "rb") as f:
                    audio_bytes = f.read()
                os.remove(output_path)
                return audio_bytes
            
            return str(output_path)
            
        except Exception as e:
            raise RuntimeError(f"Failed to synthesize speech: {str(e)}")

    def synthesize_with_voice(self, text: str, speaker_wav: Union[str, Path],
                              output_path: Optional[Union[str, Path]] = None,
                              use_default_output_dir: bool = True,
                              cfg_scale: float = 1.3,
                              seed: Optional[int] = None,
                              **kwargs) -> Union[bytes, str]:
        """
        Synthesize speech using voice cloning
        
        Args:
            text: Hindi text to convert to speech
            speaker_wav: Path to reference audio for voice cloning (required)
            output_path: Optional path to save audio file
            use_default_output_dir: Use output/vibevoice_hindi/ folder structure
            cfg_scale: Classifier-free guidance scale
            seed: Random seed for reproducibility
            **kwargs: Additional parameters
            
        Returns:
            Path to saved file if output_path provided, else audio bytes
        """
        return self.synthesize(
            text=text,
            output_path=output_path,
            speaker_wav=speaker_wav,
            use_default_output_dir=use_default_output_dir,
            cfg_scale=cfg_scale,
            seed=seed,
            **kwargs
        )

    def synthesize_conversation(self, dialogue: List[Dict[str, str]],
                                output_path: Optional[Union[str, Path]] = None,
                                use_default_output_dir: bool = True,
                                cfg_scale: float = 1.3,
                                seed: Optional[int] = None,
                                **kwargs) -> Union[bytes, str]:
        """
        Synthesize multi-speaker conversation
        
        Args:
            dialogue: List of dicts with 'speaker' and 'text' keys
                      e.g., [{"speaker": "hi-Priya_woman", "text": "नमस्ते"},
                             {"speaker": "hi-Raj_man", "text": "नमस्ते, कैसे हो?"}]
            output_path: Optional path to save audio file
            use_default_output_dir: Use output/vibevoice_hindi/ folder structure
            cfg_scale: Classifier-free guidance scale
            seed: Random seed for reproducibility
            **kwargs: Additional parameters
            
        Returns:
            Path to saved file if output_path provided, else audio bytes
        """
        if not self._initialized:
            self.initialize()
        
        try:
            import torch
            import soundfile as sf
            
            # Format dialogue for VibeVoice
            formatted_text = ""
            speakers = []
            for turn in dialogue:
                speaker = turn.get("speaker", self.DEFAULT_SPEAKER)
                text = turn.get("text", "")
                if speaker not in speakers:
                    speakers.append(speaker)
                formatted_text += f"[{speaker}]: {text}\n"
            
            # Prepare output path
            if output_path is None:
                output_path = "temp_conversation.wav"
                return_bytes = True
            else:
                output_path = Path(output_path)
                if use_default_output_dir and not output_path.is_absolute():
                    output_path = Path("output") / "vibevoice_hindi" / output_path
                output_path.parent.mkdir(parents=True, exist_ok=True)
                return_bytes = False
            
            if seed is not None:
                torch.manual_seed(seed)
            
            # Generate conversation audio
            audio_output = self._pipeline.generate(
                text=formatted_text,
                speaker_names=speakers,
                cfg_scale=cfg_scale,
                **kwargs
            )
            
            if hasattr(audio_output, 'audio'):
                audio_data = audio_output.audio
                sample_rate = audio_output.sample_rate
            else:
                audio_data = audio_output
                sample_rate = 24000
            
            sf.write(str(output_path), audio_data, sample_rate)
            
            if return_bytes:
                with open(output_path, "rb") as f:
                    audio_bytes = f.read()
                os.remove(output_path)
                return audio_bytes
            
            return str(output_path)
            
        except Exception as e:
            raise RuntimeError(f"Failed to synthesize conversation: {str(e)}")

    def get_speakers(self) -> Dict[str, str]:
        """Get available Hindi speakers"""
        return self.HINDI_SPEAKERS.copy()

    def get_supported_languages(self) -> list:
        """Get list of supported language codes"""
        return ["hi"]
    
    def get_language_names(self) -> dict:
        """Get dictionary mapping language codes to names"""
        return {"hi": "Hindi"}

    def add_custom_voice(self, voice_name: str, voice_wav: Union[str, Path]) -> str:
        """
        Add a custom voice for voice cloning
        
        Args:
            voice_name: Name for the custom voice
            voice_wav: Path to the reference audio file
            
        Returns:
            Speaker ID to use in synthesize()
        """
        import shutil
        
        if not self._voices_dir:
            self._voices_dir = Path("demo/voices")
            self._voices_dir.mkdir(parents=True, exist_ok=True)
        
        # Copy voice file to voices directory
        voice_path = self._voices_dir / f"{voice_name}.wav"
        shutil.copy(str(voice_wav), str(voice_path))
        
        # Add to speakers dict
        speaker_id = f"custom-{voice_name}"
        self.HINDI_SPEAKERS[speaker_id] = f"Custom Voice ({voice_name})"
        
        print(f"Added custom voice: {speaker_id}")
        return speaker_id

    def synthesize_batch(self, texts: List[str], output_dir: Union[str, Path],
                        speaker: Optional[str] = None,
                        speaker_wav: Optional[Union[str, Path]] = None,
                        **kwargs) -> List[str]:
        """
        Synthesize multiple texts in batch
        
        Args:
            texts: List of texts to synthesize
            output_dir: Directory to save output files
            speaker: Speaker ID to use
            speaker_wav: Reference audio for voice cloning
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
                speaker=speaker,
                speaker_wav=speaker_wav,
                use_default_output_dir=False,
                **kwargs
            )
            output_paths.append(result)
        
        return output_paths
