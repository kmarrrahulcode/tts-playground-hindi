"""
Base interface for TTS engines
"""

from abc import ABC, abstractmethod
from typing import Optional, Union
from pathlib import Path


class TTSBase(ABC):
    """Base class for all TTS engines"""
    
    def __init__(self, model_name: str, device: str = "cpu"):
        """
        Initialize TTS engine
        
        Args:
            model_name: Name/identifier of the model
            device: Device to run on ('cpu' or 'cuda')
        """
        self.model_name = model_name
        self.device = device
        self._model = None
        self._initialized = False
    
    @abstractmethod
    def initialize(self):
        """Initialize the TTS model"""
        pass
    
    @abstractmethod
    def synthesize(self, text: str, output_path: Optional[Union[str, Path]] = None, 
                   **kwargs) -> Union[bytes, str]:
        """
        Synthesize speech from text
        
        Args:
            text: Text to convert to speech
            output_path: Optional path to save audio file
            **kwargs: Additional parameters specific to the TTS engine
            
        Returns:
            Audio data (bytes) or path to saved file
        """
        pass
    
    @abstractmethod
    def get_supported_languages(self) -> list:
        """Get list of supported languages"""
        pass
    
    def is_initialized(self) -> bool:
        """Check if model is initialized"""
        return self._initialized
    
    def __enter__(self):
        """Context manager entry"""
        if not self._initialized:
            self.initialize()
        return self
    
    def __exit__(self, exc_type, exc_val, exc_tb):
        """Context manager exit"""
        pass

