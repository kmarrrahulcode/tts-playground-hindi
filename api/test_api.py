"""
Test script for TTS Playground API
"""
import requests
import json

BASE_URL = "http://localhost:8000"


def test_health():
    """Test health endpoint"""
    print("\n1. Testing health endpoint...")
    response = requests.get(f"{BASE_URL}/health")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_models():
    """Test models endpoint"""
    print("\n2. Testing models endpoint...")
    response = requests.get(f"{BASE_URL}/models")
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_speakers():
    """Test speakers endpoint"""
    print("\n3. Testing speakers endpoint...")
    response = requests.get(f"{BASE_URL}/speakers?model=indri")
    print(f"Status: {response.status_code}")
    data = response.json()
    print(f"Total speakers: {data['total']}")
    print(f"First 3 speakers: {json.dumps(dict(list(data['speakers'].items())[:3]), indent=2)}")


def test_synthesize_indri():
    """Test synthesis with Indri"""
    print("\n4. Testing Indri synthesis...")
    payload = {
        "text": "नमस्ते, यह एक टेस्ट है।",
        "model": "indri",
        "output_filename": "test_indri_api.wav",
        "speaker": "[spkr_68]",
        "max_new_tokens": 4096
    }
    
    response = requests.post(f"{BASE_URL}/synthesize", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


def test_synthesize_xtts():
    """Test synthesis with XTTS"""
    print("\n5. Testing XTTS synthesis...")
    payload = {
        "text": "यह XTTS का टेस्ट है।",
        "model": "xtts-hindi",
        "output_filename": "test_xtts_api.wav",
        "language": "hi"
    }
    
    response = requests.post(f"{BASE_URL}/synthesize", json=payload)
    print(f"Status: {response.status_code}")
    print(f"Response: {json.dumps(response.json(), indent=2)}")


if __name__ == "__main__":
    print("=" * 60)
    print("TTS Playground API Test Suite")
    print("=" * 60)
    print("\nMake sure the API is running at http://localhost:8000")
    print("Start it with: python api/start_api.py")
    
    input("\nPress Enter to start tests...")
    
    try:
        test_health()
        test_models()
        test_speakers()
        test_synthesize_indri()
        # test_synthesize_xtts()  # Uncomment if you want to test XTTS
        
        print("\n" + "=" * 60)
        print("Tests completed!")
        print("=" * 60)
        
    except requests.exceptions.ConnectionError:
        print("\n❌ Error: Could not connect to API")
        print("Make sure the API is running: python api/start_api.py")
    except Exception as e:
        print(f"\n❌ Error: {str(e)}")
