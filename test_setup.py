"""
Simple test script to verify TTS Playground setup
Run this to check if everything is configured correctly
"""

import os
import sys

def test_imports():
    """Test if all required modules can be imported"""
    print("Testing imports...")
    try:
        from tts_playground import get_tts_engine, TTSBase
        from tts_playground.xtts_hindi import XTTSHindi
        from tts_playground.factory import list_available_engines
        print("✓ All imports successful")
        return True
    except ImportError as e:
        print(f"✗ Import error: {e}")
        return False

def test_environment():
    """Test environment variables"""
    print("\nTesting environment...")
    hf_token = os.getenv("HF_TOKEN")
    if hf_token:
        print(f"✓ HF_TOKEN is set (length: {len(hf_token)})")
        return True
    else:
        print("✗ HF_TOKEN is not set")
        print("  Please set it using: $env:HF_TOKEN='your_token' (PowerShell)")
        return False

def test_engine_registry():
    """Test engine registry"""
    print("\nTesting engine registry...")
    try:
        from tts_playground.factory import list_available_engines
        engines = list_available_engines()
        print(f"✓ Available engines: {engines}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_engine_creation():
    """Test creating an engine instance (without initializing)"""
    print("\nTesting engine creation...")
    try:
        from tts_playground import get_tts_engine
        
        # This should work even without HF_TOKEN (will fail on initialize)
        hf_token = os.getenv("HF_TOKEN")
        if not hf_token:
            print("  Skipping (HF_TOKEN not set)")
            return None
        
        tts = get_tts_engine("xtts-hindi", device="cpu")
        print(f"✓ Engine created: {type(tts).__name__}")
        print(f"  Model: {tts.model_name}")
        print(f"  Device: {tts.device}")
        return True
    except Exception as e:
        print(f"✗ Error: {e}")
        return False

def test_dependencies():
    """Test if required dependencies are installed"""
    print("\nTesting dependencies...")
    dependencies = {
        "TTS": "TTS",
        "torch": "torch",
        "numpy": "numpy",
        "huggingface_hub": "huggingface_hub",
    }
    
    all_ok = True
    for name, module in dependencies.items():
        try:
            __import__(module)
            print(f"✓ {name} installed")
        except ImportError:
            print(f"✗ {name} not installed")
            all_ok = False
    
    return all_ok

def main():
    """Run all tests"""
    print("=" * 50)
    print("TTS Playground Setup Verification")
    print("=" * 50)
    
    results = {
        "Imports": test_imports(),
        "Dependencies": test_dependencies(),
        "Environment": test_environment(),
        "Engine Registry": test_engine_registry(),
        "Engine Creation": test_engine_creation(),
    }
    
    print("\n" + "=" * 50)
    print("Summary")
    print("=" * 50)
    
    for test_name, result in results.items():
        status = "✓ PASS" if result else "✗ FAIL" if result is False else "⊘ SKIP"
        print(f"{test_name}: {status}")
    
    all_passed = all(r for r in results.values() if r is not None)
    
    if all_passed:
        print("\n✓ All tests passed! Setup looks good.")
        print("\nNext steps:")
        print("  1. Run: python examples/example_xtts_hindi.py")
        print("  2. Check USAGE.md for usage examples")
    else:
        print("\n✗ Some tests failed. Please fix the issues above.")
        sys.exit(1)

if __name__ == "__main__":
    main()

