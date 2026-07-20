#!/usr/bin/env python3
import requests
import json
import sys

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "jewelzufo/unsloth_granite-4.0-h-350m-GGUF"
REQUEST_TIMEOUT = 60

def check_ollama_service():
    """Check if Ollama service is running and accessible."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def query_granite(prompt, model=MODEL_NAME):
    """Query the quantized Granite model via Ollama API"""
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        data = response.json()

        print(f"\n{'='*60}")
        print(f"Model: {data.get('model')}")
        print(f"{'='*60}")
        print(data.get('response', 'No response'))
        print(f"{'='*60}")

        return data.get('response')

    except requests.exceptions.Timeout:
        print(f"Error: Request timed out after {REQUEST_TIMEOUT} seconds.")
        return None
    except requests.exceptions.ConnectionError:
        print("Error: Could not connect to Ollama service. Is it running on localhost:11434?")
        return None
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    # Pre-flight check
    if not check_ollama_service():
        print("Error: Ollama service is not running or not accessible at http://localhost:11434")
        print("Please start Ollama and try again.")
        sys.exit(1)
    
    query_granite("What is the benefit of using a quantized GGUF model on a Raspberry Pi?")
