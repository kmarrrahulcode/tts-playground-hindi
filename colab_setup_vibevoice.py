"""
Google Colab Setup Script for VibeVoice Hindi TTS
Run this in a Colab notebook with T4 GPU runtime

Usage in Colab:
    !python colab_setup_vibevoice.py

Or run cells individually:
    # Cell 1: Setup
    !git clone https://github.com/your-repo/tts-playground.git
    %cd tts-playground
    !python colab_setup_vibevoice.py --setup-only
    
    # Cell 2: Test
    !python colab_setup_vibevoice.py --test-only
"""

import subprocess
import sys
import os


def run_cmd(cmd, check=True):
    """Run shell command"""
    print(f"Running: {cmd}")
    result = subprocess.run(cmd, shell=True, check=check)
    return result.returncode == 0


def setup_environment():
    """Setup the VibeVoice environment in Colab"""
    print("="*60)
    print("Setting up VibeVoice Hindi TTS for Colab T4 GPU")
    print("="*60)
    
    # Check GPU
    print("\n1. Checking GPU...")
    run_cmd("nvidia-smi", check=False)
    
    # Install system dependencies
    print("\n2. Installing system dependencies...")
    run_cmd("apt-get update && apt-get install -y ffmpeg", check=False)
    
    # Install VibeVoice from community fork
    print("\n3. Installing VibeVoice...")
    run_cmd("pip install git+https://github.com/vibevoice-community/VibeVoice.git")
    
    # Install other dependencies
    print("\n4. Installing other dependencies...")
    run_cmd("pip install soundfile numpy huggingface_hub accelerate scipy librosa")
    run_cmd("pip install fastapi uvicorn python-multipart")
    
    # Install tts-playground in editable mode
    print("\n5. Installing tts-playground...")
    run_cmd("pip install -e .")
    
    # Create output directories
    print("\n6. Creating directories...")
    os.makedirs("output/vibevoice_hindi", exist_ok=True)
    os.makedirs("demo/voices", exist_ok=True)
    
    print("\n" + "="*60)
    print("Setup complete!")
    print("="*60)


def test_vibevoice():
    """Test VibeVoice Hindi TTS"""
    print("\n" + "="*60)
    print("Testing VibeVoice Hindi TTS")
    print("="*60)
    
    try:
        from tts_playground import get_tts_engine
        
        print("\n1. Initializing model...")
        tts = get_tts_engine("vibevoice-hindi", device="cuda")
        tts.initialize()
        
        print("\n2. Generating test audio...")
        text = "नमस्ते, यह विबवॉइस हिंदी का परीक्षण है।"
        
        output_path = tts.synthesize(
            text=text,
            output_path="test_vibevoice.wav",
            speaker="hi-Priya_woman"
        )
        
        print(f"\n3. Generated: {output_path}")
        
        # Check file size
        if os.path.exists(output_path):
            size = os.path.getsize(output_path)
            print(f"   File size: {size / 1024:.1f} KB")
        
        print("\n" + "="*60)
        print("Test successful!")
        print("="*60)
        
        return True
        
    except Exception as e:
        print(f"\nError: {e}")
        import traceback
        traceback.print_exc()
        return False


def start_api():
    """Start the API server"""
    print("\n" + "="*60)
    print("Starting TTS Playground API")
    print("="*60)
    
    # For Colab, we need to use ngrok or similar for external access
    print("\nNote: In Colab, use ngrok for external access:")
    print("  !pip install pyngrok")
    print("  from pyngrok import ngrok")
    print("  ngrok.set_auth_token('YOUR_TOKEN')")
    print("  public_url = ngrok.connect(8000)")
    print("  print(public_url)")
    
    os.chdir("api")
    run_cmd("python start_api.py")


def main():
    import argparse
    parser = argparse.ArgumentParser(description="Colab setup for VibeVoice Hindi")
    parser.add_argument("--setup-only", action="store_true", help="Only run setup")
    parser.add_argument("--test-only", action="store_true", help="Only run test")
    parser.add_argument("--api", action="store_true", help="Start API server")
    args = parser.parse_args()
    
    if args.setup_only:
        setup_environment()
    elif args.test_only:
        test_vibevoice()
    elif args.api:
        start_api()
    else:
        # Full setup and test
        setup_environment()
        test_vibevoice()


if __name__ == "__main__":
    main()
