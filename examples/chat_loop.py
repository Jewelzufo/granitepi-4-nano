#!/usr/bin/env python3
import requests
import sys

def chat_session():
    url = "http://localhost:11434/api/generate"
    model = "jewelzufo/unsloth_granite-4.0-h-350m-GGUF"
    context = []

    print(f"Starting session with {model}...")
    print("Type '/exit' to quit.\n")

    while True:
        try:
            user_input = input(">>> ")
            if user_input.lower() in ['/exit', 'quit', 'exit']:
                break

            payload = {
                "model": model,
                "prompt": user_input,
                "context": context,
                "stream": False
            }

            response = requests.post(url, json=payload, timeout=120)
            data = response.json()

            # Maintain conversation memory
            context = data.get('context', [])
            print(f"{data.get('response')}\n")

        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    chat_session()
