#!/usr/bin/env python3
import requests
import json

def query_granite(prompt, model="jewelzufo/unsloth_granite-4.0-h-350m-GGUF"):
    """Query the quantized Granite model via Ollama API"""
    url = "http://localhost:11434/api/generate"

    payload = {
        "model": model,
        "prompt": prompt,
        "stream": False
    }

    try:
        response = requests.post(url, json=payload, timeout=60)
        response.raise_for_status()
        data = response.json()

        print(f"\n{'='*60}")
        print(f"Model: {data.get('model')}")
        print(f"{'='*60}")
        print(data.get('response', 'No response'))
        print(f"{'='*60}")

        return data.get('response')

    except Exception as e:
        print(f"Error: {e}")
        return None

if __name__ == "__main__":
    query_granite("What is the benefit of using a quantized GGUF model on a Raspberry Pi?")
