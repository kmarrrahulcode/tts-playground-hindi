"""
Setup script for TTS Playground - Indic Parler only
Use this for venv-parler (Python 3.13 compatible)
"""

from setuptools import setup, find_packages
from pathlib import Path

readme_file = Path(__file__).parent / "README.md"
long_description = readme_file.read_text(encoding="utf-8") if readme_file.exists() else ""

setup(
    name="tts-playground",
    version="0.1.0",
    description="A reusable Python module for Text-to-Speech libraries with Hindi support",
    long_description=long_description,
    long_description_content_type="text/markdown",
    packages=find_packages(),
    install_requires=[
        "parler-tts==0.2.3",
        "torch>=2.0.0",
        "torchaudio>=2.0.0",
        "numpy>=1.24.0",
        "soundfile>=0.12.0",
    ],
    python_requires=">=3.9",
)
