#!/usr/bin/env python3
"""
Secure Groq API Test Script (Fixed)
Tests Groq API connectivity using environment variables
Includes proper User-Agent to avoid Cloudflare blocking
"""

import os
import json
import urllib.request
import urllib.error
from dotenv import load_dotenv
from typing import Optional

load_dotenv()

def test_groq_api(api_key: Optional[str] = None) -> bool:
    """
    Test Groq API connectivity by listing available models
    
    Args:
        api_key: Optional API key. If not provided, reads from GROQ_API_KEY env var
        
    Returns:
        True if successful, False otherwise
    """
    # Get API key from parameter or environment
    api_key = api_key or os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found in environment variables")
        print("   Set it with: export GROQ_API_KEY='gsk_**************************************************'")
        return False
    
    # Test 1: List available models
    print("🔍 Testing Groq API - Listing available models...")
    url = "https://api.groq.com/openai/v1/models"
    
    headers = {
        "Authorization": f"Bearer {api_key}",
        "Content-Type": "application/json",
        "User-Agent": "python-urllib/groq-api-client"  # THIS WAS MISSING - fixes Cloudflare 403
    }
    
    try:
        req = urllib.request.Request(url, headers=headers)
        with urllib.request.urlopen(req, timeout=10) as resp:
            response = json.loads(resp.read().decode('utf-8'))
            print("✅ Success! Available models:")
            for model in response.get('data', []):
                print(f"   - {model['id']}")
            print()
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='ignore')
        print(f"❌ HTTP Error {e.code}:")
        print(f"   {error_body}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False
    
    # Test 2: Make a simple chat completion request
    print("🔍 Testing Groq API - Chat completion...")
    completion_url = "https://api.groq.com/openai/v1/chat/completions"
    
    payload = {
        "model": "llama-3.1-8b-instant",
        "messages": [
            {"role": "user", "content": "Say 'API test successful' if you can read this."}
        ],
        "temperature": 0.7,
        "max_tokens": 50
    }
    
    try:
        data = json.dumps(payload).encode('utf-8')
        req = urllib.request.Request(
            completion_url,
            data=data,
            headers=headers,
            method='POST'
        )
        
        with urllib.request.urlopen(req, timeout=30) as resp:
            response = json.loads(resp.read().decode('utf-8'))
            assistant_message = response['choices'][0]['message']['content']
            print(f"✅ Chat completion successful!")
            print(f"   Response: {assistant_message}")
            print(f"   Model: {response.get('model')}")
            print(f"   Tokens used: {response.get('usage', {}).get('total_tokens', 'N/A')}")
            print()
            return True
            
    except urllib.error.HTTPError as e:
        error_body = e.read().decode('utf-8', errors='ignore')
        print(f"❌ HTTP Error {e.code}:")
        try:
            error_json = json.loads(error_body)
            print(f"   Error: {error_json.get('error', {}).get('message', error_body)}")
        except:
            print(f"   {error_body}")
        return False
    except KeyError as e:
        print(f"❌ Unexpected response format: {e}")
        print(f"   Response: {response}")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False


def test_with_different_models(api_key: Optional[str] = None) -> None:
    """Test multiple Groq models"""
    api_key = api_key or os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found")
        return
    
    models_to_test = [
        "llama-3.1-8b-instant",
        "llama-3.1-70b-versatile",
        "mixtral-8x7b-32768",
        "gemma2-9b-it"
    ]
    
    print("🧪 Testing different models...")
    print()
    
    for model in models_to_test:
        print(f"Testing {model}...")
        
        url = "https://api.groq.com/openai/v1/chat/completions"
        headers = {
            "Authorization": f"Bearer {api_key}",
            "Content-Type": "application/json",
            "User-Agent": "python-urllib/groq-api-client"
        }
        
        payload = {
            "model": model,
            "messages": [{"role": "user", "content": "Hi"}],
            "max_tokens": 10
        }
        
        try:
            data = json.dumps(payload).encode('utf-8')
            req = urllib.request.Request(url, data=data, headers=headers, method='POST')
            
            with urllib.request.urlopen(req, timeout=30) as resp:
                response = json.loads(resp.read().decode('utf-8'))
                tokens = response.get('usage', {}).get('total_tokens', 'N/A')
                print(f"   ✅ {model}: Working! (tokens: {tokens})")
                
        except urllib.error.HTTPError as e:
            error_body = e.read().decode('utf-8', errors='ignore')
            try:
                error_json = json.loads(error_body)
                error_msg = error_json.get('error', {}).get('message', 'Unknown error')
                print(f"   ❌ {model}: {e.code} - {error_msg}")
            except:
                print(f"   ❌ {model}: HTTP {e.code}")
        except Exception as e:
            print(f"   ❌ {model}: {str(e)}")
    
    print()


def simulate_lambda_handler_call(api_key: Optional[str] = None) -> None:
    """Simulate how Lambda handler.py calls Groq API"""
    api_key = api_key or os.environ.get("GROQ_API_KEY")
    
    if not api_key:
        print("❌ Error: GROQ_API_KEY not found")
        return
    
    print("🔍 Simulating Lambda handler.py Groq API call...")
    print()
    
    # Replicate the exact call from handler.py
    url = "https://api.groq.com/openai/v1/chat/completions"
    model = "llama-3.1-8b-instant"
    
    messages = [
        {
            "role": "system",
            "content": (
                "You are a helpful, friendly AI assistant in a Telegram bot. "
                "Be concise but informative. Use emojis occasionally to be friendly."
            )
        },
        {
            "role": "user",
            "content": "Hello! Can you introduce yourself?"
        }
    ]
    
    payload = {
        "model": model,
        "messages": messages,
        "temperature": 0.7,
        "max_tokens": 1024,
        "top_p": 1,
        "stream": False
    }
    
    data = json.dumps(payload).encode("utf-8")
    req = urllib.request.Request(url, data=data, method="POST")
    req.add_header("Content-Type", "application/json")
    req.add_header("Authorization", f"Bearer {api_key}")
    req.add_header("User-Agent", "python-urllib/groq-api-client")  # CRITICAL FIX
    
    try:
        with urllib.request.urlopen(req, timeout=30) as resp:
            resp_data = json.loads(resp.read().decode("utf-8"))
        
        print("✅ Lambda-style call successful!")
        print(f"   Model: {resp_data.get('model')}")
        print(f"   Tokens: {resp_data.get('usage', {}).get('total_tokens', 'N/A')}")
        print(f"   Response: {resp_data['choices'][0]['message']['content'][:200]}...")
        print()
        
    except urllib.error.HTTPError as e:
        error_body = e.read().decode("utf-8", errors="ignore")
        print(f"❌ HTTP Error {e.code}:")
        try:
            error_json = json.loads(error_body)
            print(f"   {json.dumps(error_json, indent=2)}")
        except:
            print(f"   {error_body}")
    except Exception as e:
        print(f"❌ Error: {type(e).__name__}: {e}")


if __name__ == "__main__":
    import sys
    
    print("=" * 60)
    print("Groq API Connectivity Test (FIXED)")
    print("=" * 60)
    print()
    
    # Check if API key is provided as command line argument (for testing only)
    api_key = None
    if len(sys.argv) > 1:
        api_key = sys.argv[1]
        print("⚠️  Warning: Using API key from command line argument")
        print("   This is for testing only. Use environment variables in production.")
        print()
    
    # Run tests
    success = test_groq_api(api_key)
    
    if success:
        print()
        simulate_lambda_handler_call(api_key)
        
        # Optionally test multiple models
        # test_with_different_models(api_key)
    
    print("=" * 60)
    print("Test completed")
    print("=" * 60)