"""
Indri TTS Implementation
A lightweight TTS model based on GPT-2 architecture
Supports English and Hindi with voice cloning
"""

import os
import torch
import torchaudio
import soundfile as sf
from pathlib import Path
from typing import Optional, Union, List
from transformers import pipeline

from tts_playground.base import TTSBase


class IndriTTS(TTSBase):
    """
    Indri TTS Engine
    
    Model: 11mlabs/indri-0.1-350m-tts
    Supports: English and Hindi
    Features: 13 pre-trained speakers, code-mixing support
    Note: Does NOT support voice cloning from audio files (only pre-trained speakers)
    """
    
    # Available speakers from the model
    AVAILABLE_SPEAKERS = {
        "[spkr_63]": "🇬🇧 👨 book reader",
        "[spkr_67]": "🇺🇸 👨 influencer",
        "[spkr_68]": "🇮🇳 👨 book reader",
        "[spkr_69]": "🇮🇳 👨 book reader",
        "[spkr_70]": "🇮🇳 👨 motivational speaker",
        "[spkr_62]": "🇮🇳 👨 book reader heavy",
        "[spkr_53]": "🇮🇳 👩 recipe reciter",
        "[spkr_60]": "🇮🇳 👩 book reader",
        "[spkr_74]": "🇺🇸 👨 book reader",
        "[spkr_75]": "🇮🇳 👨 entrepreneur",
        "[spkr_76]": "🇬🇧 👨 nature lover",
        "[spkr_77]": "🇮🇳 👨 influencer",
        "[spkr_66]": "🇮🇳 👨 politician",
    }
    
    def __init__(self, model_name: str = "11mlabs/indri-0.1-350m-tts",
                 device: str = "cpu", hf_token: Optional[str] = None):
        """
        Initialize Indri TTS engine
        
        Args:
            model_name: HuggingFace model name
            device: Device to run on ('cpu' or 'cuda')
            hf_token: HuggingFace token (if None, reads from HF_TOKEN env var)
        """
        super().__init__(model_name, device)
        self.hf_token = hf_token or os.getenv("HF_TOKEN")
        
        # Set device for torch
        if device == "cpu":
            self.torch_device = "cpu"
        else:
            self.torch_device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Default speaker
        self.default_speaker = "[spkr_68]"  # Hindi book reader
    
    def initialize(self):
        """Initialize the Indri TTS model"""
        if self._initialized:
            return
        
        try:
            print(f"Loading Indri TTS model: {self.model_name}")
            print(f"Device: {self.torch_device}")
            
            # Create pipeline
            self._model = pipeline(
                "indri-tts",
                model=self.model_name,
                device=torch.device(self.torch_device),
                trust_remote_code=True,
                token=self.hf_token
            )
            
            self._initialized = True
            print("Indri TTS model loaded successfully!")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize Indri TTS model: {str(e)}")
    
    def synthesize(self, text: str, output_path: Optional[Union[str, Path]] = None,
                   speaker: Optional[str] = None,
                   language: Optional[str] = None,
                   speaker_wav: Optional[Union[str, Path]] = None,
                   use_default_output_dir: bool = True,
                   **kwargs) -> Union[bytes, str]:
        """
        Synthesize speech from text
        
        Args:
            text: Text to convert to speech (supports English and Hindi, code-mixing OK)
            output_path: Optional path to save audio file (if None, returns bytes)
            speaker: Speaker ID (e.g., "[spkr_68]"). If None, uses default speaker.
                    Use get_available_speakers() to see all options.
            language: Language code (optional, model auto-detects)
            speaker_wav: NOT SUPPORTED - Indri does not support voice cloning from audio files.
                        This parameter is kept for API compatibility but will be ignored with a warning.
                        Use the 'speaker' parameter instead to select from 13 pre-trained speakers.
            **kwargs: Additional parameters:
                - max_new_tokens (int): Maximum length of generated audio tokens (default: 2048)
                                       Increase for longer text (e.g., 4096, 8192)
                - temperature (float): Sampling temperature (default: 1.0)
                - do_sample (bool): Whether to use sampling (default: True)
            
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
                
                # Add default output directory structure if requested
                if use_default_output_dir and not output_path.is_absolute():
                    output_path = Path("output") / "indri" / output_path
                
                output_path.parent.mkdir(parents=True, exist_ok=True)
                return_bytes = False
            
            # Prepare synthesis parameters
            synthesis_kwargs = {}
            
            # Note: Indri does NOT support voice cloning from audio files
            # It only supports pre-trained speaker IDs
            if speaker_wav:
                print("Warning: Indri TTS does not support voice cloning from audio files.")
                print("         Using default speaker instead. Use 'speaker' parameter to select")
                print("         from 13 pre-trained speakers. See get_available_speakers().")
            
            # Use speaker ID (only supported method)
            speaker_id = speaker or self.default_speaker
            synthesis_kwargs['speaker'] = speaker_id
            
            # Add generation parameters to avoid truncation
            # max_new_tokens controls the maximum length of generated audio
            generation_kwargs = {
                'max_new_tokens': kwargs.get('max_new_tokens', 2048),  # Increased from default
                'do_sample': kwargs.get('do_sample', True),
                'temperature': kwargs.get('temperature', 1.0),
            }
            
            # Merge with synthesis kwargs
            synthesis_kwargs.update(generation_kwargs)
            
            # Synthesize speech
            # Pipeline expects a list of texts
            result = self._model([text], **synthesis_kwargs)
            
            # Extract audio from result
            # The pipeline returns a list of dicts with 'audio' key
            if isinstance(result, list) and len(result) > 0:
                audio_data = result[0].get('audio', result[0])
                
                # Handle different return formats
                if isinstance(audio_data, tuple):
                    audio_tensor, sample_rate = audio_data
                elif isinstance(audio_data, dict):
                    audio_tensor = audio_data.get('audio', audio_data)
                    sample_rate = audio_data.get('sample_rate', 24000)
                else:
                    audio_tensor = audio_data
                    sample_rate = 24000  # Default sample rate for Indri
                
                # Ensure audio_tensor is a torch tensor
                if not isinstance(audio_tensor, torch.Tensor):
                    raise ValueError(f"Unexpected audio format: {type(audio_tensor)}")
                
                # Convert to numpy and save using soundfile (avoids torchcodec dependency)
                audio_numpy = audio_tensor.cpu().numpy()
                
                # Ensure correct shape: soundfile expects (samples,) or (samples, channels)
                # Remove all dimensions of size 1
                audio_numpy = audio_numpy.squeeze()
                
                # If still multi-dimensional and first dim is small (likely channels), transpose
                if audio_numpy.ndim == 2 and audio_numpy.shape[0] < audio_numpy.shape[1]:
                    audio_numpy = audio_numpy.T
                
                sf.write(str(output_path), audio_numpy, sample_rate)
                
                # Return bytes if no output path was provided
                if return_bytes:
                    with open(output_path, "rb") as f:
                        audio_bytes = f.read()
                    os.remove(output_path)  # Clean up temp file
                    return audio_bytes
                
                return str(output_path)
            else:
                raise RuntimeError("Pipeline returned empty result")
            
        except Exception as e:
            raise RuntimeError(f"Failed to synthesize speech: {str(e)}")
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return ["en", "hi"]  # English and Hindi
    
    def get_available_speakers(self) -> dict:
        """
        Get dictionary of available speakers
        
        Returns:
            Dictionary mapping speaker IDs to descriptions
        """
        return self.AVAILABLE_SPEAKERS.copy()
    
    def synthesize_batch(self, texts: List[str], output_dir: Union[str, Path],
                        speaker: Optional[str] = None,
                        speaker_wav: Optional[Union[str, Path]] = None,
                        **kwargs) -> List[str]:
        """
        Synthesize multiple texts in batch
        
        Args:
            texts: List of texts to synthesize
            output_dir: Directory to save output files
            speaker: Speaker ID (optional)
            speaker_wav: Optional path to reference audio for voice cloning
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
                **kwargs
            )
            output_paths.append(result)
        
        return output_paths

