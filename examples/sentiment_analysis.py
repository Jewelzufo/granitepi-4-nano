#!/usr/bin/env python3
import requests
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

def analyze_sentiment(text):
    """
    Performs sentiment analysis using the IBM Granite 4.0 model via the local Ollama API.
    """
    # System prompt to instruct the model to act as a sentiment analyzer
    prompt = (
        f"Analyze the sentiment of the following text. "
        f"Respond with only one word: Positive, Negative, or Neutral.\n\n"
        f"Text: \"{text}\"\n"
        f"Sentiment:"
    )

    payload = {
        "model": MODEL_NAME,
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0  # Set to 0 for deterministic, consistent results
        }
    }

    try:
        response = requests.post(OLLAMA_URL, json=payload, timeout=REQUEST_TIMEOUT)
        response.raise_for_status()
        result = response.json()
        return result['response'].strip()
    except requests.exceptions.Timeout:
        return f"Error: Request timed out after {REQUEST_TIMEOUT} seconds."
    except requests.exceptions.ConnectionError:
        return "Error: Could not connect to Ollama service. Is it running on localhost:11434?"
    except requests.exceptions.HTTPError as e:
        return f"HTTP error occurred: {e}"
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}"

if __name__ == "__main__":
    # Pre-flight check
    if not check_ollama_service():
        print("Error: Ollama service is not running or not accessible at http://localhost:11434")
        print("Please start Ollama and try again.")
        sys.exit(1)

    print("--- Granite 4.0 Sentiment Analyzer ---")
    print("Type 'exit' to quit.")

    while True:
        try:
            user_input = input("\nEnter text to analyze: ")
            if user_input.lower() == 'exit':
                break

            sentiment = analyze_sentiment(user_input)
            print(f"Detected Sentiment: {sentiment}")
        except KeyboardInterrupt:
            print("\nExiting...")
            break
        except EOFError:
            break
