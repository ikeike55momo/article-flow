#!/usr/bin/env python3
"""Test script for gpt-image-1 API implementation"""

import os
import sys
import base64
from pathlib import Path

# Test with OpenAI library
def test_openai_library():
    """Test using official OpenAI library"""
    try:
        from openai import OpenAI
        
        client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))
        
        prompt = "A serene mountain landscape at sunset with soft pastel colors"
        
        print("Testing with OpenAI library...")
        result = client.images.generate(
            model="gpt-image-1",
            prompt=prompt,
            n=1,
            size="1024x1024",
            quality="high"
            # Note: NO response_format parameter!
        )
        
        # Get base64 data
        image_b64 = result.data[0].b64_json
        image_bytes = base64.b64decode(image_b64)
        
        # Save test image
        with open("test_openai_library.png", "wb") as f:
            f.write(image_bytes)
        
        print("✓ OpenAI library test successful!")
        print(f"  - Image saved to: test_openai_library.png")
        print(f"  - Size: {len(image_bytes):,} bytes")
        
    except Exception as e:
        print(f"✗ OpenAI library test failed: {e}")
        return False
    
    return True

# Test with raw requests
def test_raw_requests():
    """Test using raw requests to API"""
    import requests
    
    api_key = os.getenv("OPENAI_API_KEY")
    if not api_key:
        print("✗ OPENAI_API_KEY not found in environment")
        return False
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json"
    }
    
    data = {
        "model": "gpt-image-1",
        "prompt": "A cute cartoon robot holding a sign that says 'Hello World'",
        "n": 1,
        "size": "1024x1024",
        "quality": "high"
        # NO response_format parameter!
    }
    
    print("\nTesting with raw requests...")
    try:
        response = requests.post(
            "https://api.openai.com/v1/images/generations",
            headers=headers,
            json=data,
            timeout=30
        )
        
        if response.status_code == 200:
            result = response.json()
            
            # Get base64 data
            image_b64 = result['data'][0]['b64_json']
            image_bytes = base64.b64decode(image_b64)
            
            # Save test image
            with open("test_raw_requests.png", "wb") as f:
                f.write(image_bytes)
            
            print("✓ Raw requests test successful!")
            print(f"  - Image saved to: test_raw_requests.png")
            print(f"  - Size: {len(image_bytes):,} bytes")
            
            # Check for revised prompt
            if 'revised_prompt' in result['data'][0]:
                print(f"  - Revised prompt: {result['data'][0]['revised_prompt'][:50]}...")
        else:
            error_msg = response.json().get('error', {}).get('message', response.text)
            print(f"✗ API Error {response.status_code}: {error_msg}")
            return False
            
    except Exception as e:
        print(f"✗ Raw requests test failed: {e}")
        return False
    
    return True

# Test different sizes
def test_sizes():
    """Test different supported sizes"""
    import requests
    
    api_key = os.getenv("OPENAI_API_KEY")
    sizes = ["1024x1024", "1024x1536", "1536x1024"]
    
    print("\nTesting different sizes...")
    for size in sizes:
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-image-1",
                "prompt": f"A test image in {size} format",
                "size": size,
                "quality": "high"
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"  ✓ Size {size} supported")
            else:
                error = response.json().get('error', {}).get('message', 'Unknown error')
                print(f"  ✗ Size {size} failed: {error}")
                
        except Exception as e:
            print(f"  ✗ Size {size} error: {e}")

# Test quality options
def test_quality():
    """Test quality options"""
    import requests
    
    api_key = os.getenv("OPENAI_API_KEY")
    qualities = ["low", "medium", "high", "auto"]
    
    print("\nTesting quality options...")
    for quality in qualities:
        try:
            headers = {
                "Authorization": f"Bearer {api_key}",
                "Content-Type": "application/json"
            }
            
            data = {
                "model": "gpt-image-1",
                "prompt": f"A test image with {quality} quality",
                "size": "1024x1024",
                "quality": quality
            }
            
            response = requests.post(
                "https://api.openai.com/v1/images/generations",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                print(f"  ✓ Quality '{quality}' supported")
            else:
                error = response.json().get('error', {}).get('message', 'Unknown error')
                print(f"  ✗ Quality '{quality}' failed: {error}")
                
        except Exception as e:
            print(f"  ✗ Quality '{quality}' error: {e}")

# Main test runner
def main():
    print("=== GPT-Image-1 API Test Suite ===\n")
    
    if not os.getenv("OPENAI_API_KEY"):
        print("Error: OPENAI_API_KEY environment variable not set")
        sys.exit(1)
    
    # Run tests
    tests_passed = 0
    total_tests = 4
    
    if test_openai_library():
        tests_passed += 1
    
    if test_raw_requests():
        tests_passed += 1
    
    test_sizes()  # Info only
    test_quality()  # Info only
    
    print(f"\n=== Test Results: {tests_passed}/2 core tests passed ===")
    
    if tests_passed == 2:
        print("\nAll core tests passed! The gpt-image-1 implementation should work correctly.")
        print("\nKey findings:")
        print("- gpt-image-1 always returns base64 data (no URL option)")
        print("- Do NOT include 'response_format' parameter")
        print("- Supported sizes: 1024x1024, 1024x1536, 1536x1024")
        print("- Quality options: 'low', 'medium', 'high', or 'auto'")
    else:
        print("\nSome tests failed. Please check the error messages above.")

if __name__ == "__main__":
    main()