import requests
import json

def analyze_sentiment(text):
    """
    Performs sentiment analysis using the IBM Granite 4.0 model via the local Ollama API.
    """
    url = "http://localhost:11434/api/generate"

    # System prompt to instruct the model to act as a sentiment analyzer
    prompt = (
        f"Analyze the sentiment of the following text. "
        f"Respond with only one word: Positive, Negative, or Neutral.\n\n"
        f"Text: \"{text}\"\n"
        f"Sentiment:"
    )

    payload = {
        "model": "jewelzufo/unsloth_granite-4.0-h-350m-GGUF",
        "prompt": prompt,
        "stream": False,
        "options": {
            "temperature": 0  # Set to 0 for deterministic, consistent results
        }
    }

    try:
        response = requests.post(url, json=payload)
        response.raise_for_status()
        result = response.json()
        return result['response'].strip()
    except requests.exceptions.RequestException as e:
        return f"Error connecting to Ollama: {e}"

if __name__ == "__main__":
    print("--- Granite 4.0 Sentiment Analyzer ---")
    print("Type 'exit' to quit.")

    while True:
        user_input = input("\nEnter text to analyze: ")
        if user_input.lower() == 'exit':
            break

        sentiment = analyze_sentiment(user_input)
        print(f"Detected Sentiment: {sentiment}")
