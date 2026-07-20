#!/usr/bin/env python3
import requests
import sys

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "jewelzufo/unsloth_granite-4.0-h-350m-GGUF"
REQUEST_TIMEOUT = 120

def check_ollama_service():
    """Check if Ollama service is running and accessible."""
    try:
        response = requests.get("http://localhost:11434/api/tags", timeout=5)
        response.raise_for_status()
        return True
    except requests.exceptions.RequestException:
        return False

def chat_session():
    url = OLLAMA_URL
    model = MODEL_NAME
    context = []

    # Pre-flight check
    if not check_ollama_service():
        print("Error: Ollama service is not running or not accessible at http://localhost:11434")
        print("Please start Ollama and try again.")
        sys.exit(1)

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

            response = requests.post(url, json=payload, timeout=REQUEST_TIMEOUT)
            response.raise_for_status()
            data = response.json()

            # Maintain conversation memory
            context = data.get('context', [])
            print(f"{data.get('response')}\n")

        except requests.exceptions.Timeout:
            print(f"\nError: Request timed out after {REQUEST_TIMEOUT} seconds.")
        except requests.exceptions.ConnectionError:
            print("\nError: Lost connection to Ollama service.")
            break
        except requests.exceptions.HTTPError as e:
            print(f"\nHTTP error occurred: {e}")
        except KeyboardInterrupt:
            break
        except Exception as e:
            print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    chat_session()
