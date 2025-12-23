"""
XTTS-Hindi TTS Implementation
A CPU-optimized implementation for Hindi text-to-speech
"""

import os
import sys
from pathlib import Path
from typing import Optional, Union

# Add FFmpeg DLL directory to Windows DLL search path BEFORE importing torch/TTS
# This is needed for torchcodec to find FFmpeg DLLs on Windows
if sys.platform == "win32":
    import subprocess
    
    ffmpeg_bin_dir = None
    
    # Method 1: Try to find FFmpeg using 'where' command
    try:
        result = subprocess.run(["where", "ffmpeg"], capture_output=True, text=True, shell=True)
        if result.returncode == 0:
            ffmpeg_path = result.stdout.strip().split("\n")[0]
            ffmpeg_bin_dir = str(Path(ffmpeg_path).parent)
    except Exception:
        pass
    
    # Method 2: If not found, try common installation paths
    if not ffmpeg_bin_dir or not os.path.exists(ffmpeg_bin_dir):
        common_paths = [
            r"C:\ffmpeg\bin",
            r"C:\Program Files\ffmpeg\bin",
        ]
        # Also check for versioned folders in common locations
        for base_path in [r"C:\Softwares\ffmpeg", r"C:\ffmpeg"]:
            base = Path(base_path)
            if base.exists():
                # Look for folders starting with "ffmpeg-"
                for subdir in base.iterdir():
                    if subdir.is_dir() and subdir.name.startswith("ffmpeg-"):
                        bin_dir = subdir / "bin"
                        if bin_dir.exists():
                            common_paths.append(str(bin_dir))
                            break
        
        for path in common_paths:
            if os.path.exists(path):
                ffmpeg_bin_dir = path
                break
    
    # Add to DLL search path if found
    if ffmpeg_bin_dir and os.path.exists(ffmpeg_bin_dir):
        try:
            os.add_dll_directory(ffmpeg_bin_dir)
        except Exception:
            pass
        
        # Also add to PATH environment variable as a fallback
        current_path = os.environ.get("PATH", "")
        if ffmpeg_bin_dir not in current_path:
            os.environ["PATH"] = ffmpeg_bin_dir + os.pathsep + current_path
        
        # Copy FFmpeg DLLs to torchcodec package directory if needed
        # This ensures torchcodec DLLs can find FFmpeg DLLs at load time
        try:
            import site
            site_packages = site.getsitepackages()[0] if site.getsitepackages() else None
            if site_packages:
                torchcodec_dir = Path(site_packages) / "torchcodec"
                if torchcodec_dir.exists():
                    # Copy essential FFmpeg DLLs to torchcodec directory
                    ffmpeg_dlls = [
                        "avcodec-*.dll",
                        "avformat-*.dll",
                        "avutil-*.dll",
                        "swresample-*.dll",
                        "swscale-*.dll",
                    ]
                    import shutil
                    import glob
                    copied = False
                    for pattern in ffmpeg_dlls:
                        for dll_path in glob.glob(str(Path(ffmpeg_bin_dir) / pattern)):
                            dll_name = Path(dll_path).name
                            dest_path = torchcodec_dir / dll_name
                            if not dest_path.exists():
                                try:
                                    shutil.copy2(dll_path, dest_path)
                                    copied = True
                                except Exception:
                                    pass
                    if copied:
                        # Also add torchcodec directory to DLL search path
                        try:
                            os.add_dll_directory(str(torchcodec_dir))
                        except Exception:
                            pass
        except Exception:
            # If copying fails, we'll rely on PATH and os.add_dll_directory
            pass

# Now import torch and TTS after setting up DLL paths
import torch
from TTS.api import TTS
from huggingface_hub import login, snapshot_download

from tts_playground.base import TTSBase


class XTTSHindi(TTSBase):
    """
    XTTS-Hindi TTS Engine
    
    Model: Abhinay45/XTTS-Hindi-finetuned
    Optimized for CPU usage
    """
    
    def __init__(self, model_name: str = "Abhinay45/XTTS-Hindi-finetuned", 
                 device: str = "cpu", hf_token: Optional[str] = None):
        """
        Initialize XTTS-Hindi TTS engine
        
        Args:
            model_name: HuggingFace model name
            device: Device to run on ('cpu' or 'cuda')
            hf_token: HuggingFace token (if None, reads from HF_TOKEN env var)
        """
        super().__init__(model_name, device)
        self.hf_token = hf_token or os.getenv("HF_TOKEN")
        if not self.hf_token:
            raise ValueError(
                "HuggingFace token is required. "
                "Set HF_TOKEN environment variable or pass hf_token parameter."
            )
        
        # Set device for torch
        if device == "cpu":
            self.torch_device = "cpu"
        else:
            self.torch_device = "cuda" if torch.cuda.is_available() else "cpu"
        
        # Store model directory path for finding default speaker files
        self._model_dir = None
        self._default_speaker_wav = None
    
    def initialize(self):
        """Initialize the XTTS-Hindi model"""
        if self._initialized:
            return
        
        try:
            print(f"Loading XTTS-Hindi model: {self.model_name}")
            print(f"Device: {self.torch_device}")
            
            # Login to HuggingFace if token is provided
            # This ensures we can access gated models
            if self.hf_token:
                try:
                    login(token=self.hf_token, add_to_git_credential=False)
                except Exception as e:
                    print(f"Warning: Could not login to HuggingFace: {e}")
                    print("Attempting to continue without explicit login...")
            
            # Download model from HuggingFace
            print("Downloading model from HuggingFace...")
            model_cache_dir = snapshot_download(
                repo_id=self.model_name,
                token=self.hf_token,
                cache_dir=None  # Use default cache
            )
            
            # Find model checkpoint and config files
            model_dir = Path(model_cache_dir)
            
            # Look for common model file patterns
            model_path = None
            config_path = None
            
            # Check for config.json first
            config_file = model_dir / "config.json"
            if config_file.exists():
                config_path = str(config_file)
            
            # Prioritize model.pth, then check for other model files
            # XTTS models typically have model.pth as the main checkpoint
            priority_files = ["model.pth", "model.pt", "best_model.pth"]
            for filename in priority_files:
                file_path = model_dir / filename
                if file_path.exists():
                    model_path = str(file_path)
                    break
            
            # If priority files not found, search for any .pth or .pt files
            # but exclude dvae.pth and speakers_xtts.pth as they are not the main model
            if model_path is None:
                excluded_names = {"dvae.pth", "speakers_xtts.pth", "mel_stats.pth"}
                for pattern in ["*.pth", "*.pt"]:
                    matches = list(model_dir.glob(pattern))
                    for match in matches:
                        if match.name not in excluded_names:
                            model_path = str(match)
                            break
                    if model_path:
                        break
            
            # If model_path still not found, try to find it in subdirectories
            if model_path is None:
                for subdir in model_dir.iterdir():
                    if subdir.is_dir():
                        # Check priority files first
                        for filename in priority_files:
                            file_path = subdir / filename
                            if file_path.exists():
                                model_path = str(file_path)
                                # Check for config in same directory
                                sub_config = subdir / "config.json"
                                if sub_config.exists() and config_path is None:
                                    config_path = str(sub_config)
                                break
                        if model_path:
                            break
                        
                        # If not found, search for any .pth files (excluding excluded ones)
                        if model_path is None:
                            excluded_names = {"dvae.pth", "speakers_xtts.pth", "mel_stats.pth"}
                            for pattern in ["*.pth", "*.pt"]:
                                matches = list(subdir.glob(pattern))
                                for match in matches:
                                    if match.name not in excluded_names:
                                        model_path = str(match)
                                        sub_config = subdir / "config.json"
                                        if sub_config.exists() and config_path is None:
                                            config_path = str(sub_config)
                                        break
                                if model_path:
                                    break
                        if model_path:
                            break
            
            if model_path is None:
                raise RuntimeError(
                    f"Could not find model checkpoint file in {model_dir}. "
                    f"Please check the model repository structure."
                )
            
            if config_path is None:
                print(f"Warning: config.json not found. Attempting to load without explicit config...")
            
            # For XTTS models, TTS library expects the directory path, not the file path
            # It will look for model.pth inside the directory
            model_dir_path = str(Path(model_path).parent)
            self._model_dir = Path(model_dir_path)
            
            print(f"Model directory: {model_dir_path}")
            print(f"Model file: {Path(model_path).name}")
            if config_path:
                print(f"Config path: {config_path}")
            
            # Find a default speaker reference audio file for voice cloning
            # XTTS models typically include reference speaker files
            speaker_file_patterns = ["*.wav", "*.flac", "*.mp3"]
            for pattern in speaker_file_patterns:
                matches = list(self._model_dir.glob(pattern))
                # Prefer files that look like speaker references (not too large, common names)
                for match in matches:
                    # Skip very large files (likely not reference audio)
                    if match.stat().st_size < 10 * 1024 * 1024:  # Less than 10MB
                        # Prefer files with "speaker" or "voice" in name, or common reference names
                        name_lower = match.name.lower()
                        if any(keyword in name_lower for keyword in ["speaker", "voice", "reference", "sample"]):
                            self._default_speaker_wav = str(match)
                            print(f"Found default speaker reference: {match.name}")
                            break
                if self._default_speaker_wav:
                    break
                
                # If no preferred file found, use first audio file
                if not self._default_speaker_wav and matches:
                    # Use first file that's reasonably sized
                    for match in matches:
                        if match.stat().st_size < 10 * 1024 * 1024:
                            self._default_speaker_wav = str(match)
                            print(f"Using default speaker reference: {match.name}")
                            break
            
            # Initialize TTS with the downloaded model
            # For XTTS, pass the directory containing model.pth
            init_kwargs = {
                "model_path": model_dir_path,
                "progress_bar": True,
                "gpu": (self.torch_device == "cuda")
            }
            
            if config_path:
                init_kwargs["config_path"] = config_path
            
            self._model = TTS(**init_kwargs)
            
            self._initialized = True
            print("XTTS-Hindi model loaded successfully!")
            
        except Exception as e:
            raise RuntimeError(f"Failed to initialize XTTS-Hindi model: {str(e)}")
    
    def synthesize(self, text: str, output_path: Optional[Union[str, Path]] = None,
                   speaker_wav: Optional[Union[str, Path]] = None,
                   language: str = "hi",
                   use_default_output_dir: bool = True,
                   split_sentences: bool = True,
                   **kwargs) -> Union[bytes, str]:
        """
        Synthesize speech from Hindi text
        
        Args:
            text: Hindi text to convert to speech
            output_path: Optional path to save audio file (if None, returns bytes)
            speaker_wav: Optional path to reference speaker audio for voice cloning
            language: Language code (default: "hi" for Hindi)
            use_default_output_dir: If True, saves to output/xtts_hindi/ folder (default: True)
            split_sentences: If True, splits text into sentences before synthesis (default: True)
            **kwargs: Additional parameters
            
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
                    output_path = Path("output") / "xtts_hindi" / output_path
                
                output_path.parent.mkdir(parents=True, exist_ok=True)
                return_bytes = False
            
            # Synthesize speech
            # XTTS is a voice cloning model, so it requires speaker_wav
            # If not provided, use default speaker reference file
            if not speaker_wav:
                speaker_wav = self._default_speaker_wav
                if not speaker_wav:
                    raise ValueError(
                        "XTTS-Hindi requires a speaker reference audio file (speaker_wav). "
                        "Either provide speaker_wav parameter or ensure the model includes reference audio files."
                    )
            
            # Voice cloning mode with speaker_wav
            self._model.tts_to_file(
                text=text,
                file_path=str(output_path),
                speaker_wav=speaker_wav,
                language=language,
                split_sentences=split_sentences,
                **kwargs
            )
            
            # Return bytes if no output path was provided
            if return_bytes:
                with open(output_path, "rb") as f:
                    audio_bytes = f.read()
                os.remove(output_path)  # Clean up temp file
                return audio_bytes
            
            return str(output_path)
            
        except Exception as e:
            raise RuntimeError(f"Failed to synthesize speech: {str(e)}")
    
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        return ["hi"]  # Hindi
    
    def synthesize_batch(self, texts: list, output_dir: Union[str, Path],
                        speaker_wav: Optional[Union[str, Path]] = None,
                        language: str = "hi", **kwargs) -> list:
        """
        Synthesize multiple texts in batch
        
        Args:
            texts: List of texts to synthesize
            output_dir: Directory to save output files
            speaker_wav: Optional reference speaker audio
            language: Language code
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
                language=language,
                **kwargs
            )
            output_paths.append(result)
        
        return output_paths

