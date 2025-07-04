#!/usr/bin/env python3
"""
Debug script to test PDF upload and identify the pattern matching error
"""

import requests
import tempfile
import os

def test_upload():
    """Test the upload endpoint with a simple text file"""
    
    # Create a simple test file
    with tempfile.NamedTemporaryFile(mode='w', suffix='.txt', delete=False) as f:
        f.write("This is a test document for debugging.")
        temp_file = f.name
    
    try:
        # Test with a valid API key format
        api_key = "sk-1234567890abcdef1234567890abcdef1234567890abcdef"
        
        print(f"Testing upload with file: {temp_file}")
        print(f"API key: {api_key[:10]}...")
        
        with open(temp_file, 'rb') as f:
            files = {'file': ('test.txt', f, 'text/plain')}
            data = {'api_key': api_key}
            
            response = requests.post(
                'http://localhost:8000/api/upload-pdf',
                files=files,
                data=data
            )
        
        print(f"Response status: {response.status_code}")
        print(f"Response headers: {dict(response.headers)}")
        
        if response.status_code != 200:
            print(f"Error response: {response.text}")
        else:
            print(f"Success response: {response.json()}")
            
    except Exception as e:
        print(f"Exception occurred: {e}")
        print(f"Exception type: {type(e)}")
        import traceback
        traceback.print_exc()
    
    finally:
        # Clean up
        if os.path.exists(temp_file):
            os.unlink(temp_file)

def test_health():
    """Test the health endpoint"""
    try:
        response = requests.get('http://localhost:8000/api/health')
        print(f"Health check status: {response.status_code}")
        print(f"Health check response: {response.json()}")
    except Exception as e:
        print(f"Health check failed: {e}")

if __name__ == "__main__":
    print("=== Testing Health Endpoint ===")
    test_health()
    
    print("\n=== Testing Upload Endpoint ===")
    test_upload() 