#!/usr/bin/env python3
import requests
import sys
import os
import logging
from typing import List, Dict

# Configuration
OLLAMA_URL = "http://localhost:11434/api/generate"
MODEL_NAME = "jewelzufo/unsloth_granite-4.0-h-350m-GGUF"
MAX_CONTEXT_CHARS = 8000  # Conservative limit to keep prompt efficient

logging.basicConfig(format='%(levelname)s: %(message)s', level=logging.INFO)

def load_document(filepath: str) -> str:
    """Loads and truncates document content to fit context window."""
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"File not found: {filepath}")

    try:
        with open(filepath, 'r', encoding='utf-8') as f:
            content = f.read()

        if len(content) > MAX_CONTEXT_CHARS:
            logging.warning(f"File too large. Truncating to first {MAX_CONTEXT_CHARS} characters.")
            return content[:MAX_CONTEXT_CHARS] + "\n...[TRUNCATED]"
        return content
    except Exception as e:
        raise RuntimeError(f"Failed to read file: {e}")

def chat_loop(context_text: str, filename: str):
    """Interactive chat session using the document as ground truth."""
    print(f"\n📚 Loaded: {filename}")
    print("Type '/exit' to quit.\n")

    # We keep the "system" context static, but could append conversation history if needed
    base_prompt = (
        f"You are a helpful assistant. Answer questions using ONLY the provided context below.\n"
        f"If the answer is not in the context, say 'I cannot find that information in the document.'\n\n"
        f"--- CONTEXT START ---\n{context_text}\n--- CONTEXT END ---\n"
    )

    while True:
        try:
            query = input("Question: ").strip()
            if query.lower() in ('/exit', 'exit', 'quit'):
                break
            if not query:
                continue

            full_prompt = f"{base_prompt}\nUser Question: {query}\nAnswer:"

            response = requests.post(
                OLLAMA_URL,
                json={
                    "model": MODEL_NAME,
                    "prompt": full_prompt,
                    "stream": False,
                    "options": {"temperature": 0.2}
                },
                timeout=60
            )
            response.raise_for_status()
            answer = response.json().get('response', '').strip()

            print(f"\n🤖 AI: {answer}\n")
            print("-" * 50)

        except KeyboardInterrupt:
            break
        except Exception as e:
            logging.error(f"Error during query: {e}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python3 doc_chat.py <filename>")
        sys.exit(1)

    try:
        doc_content = load_document(sys.argv[1])
        chat_loop(doc_content, sys.argv[1])
    except Exception as e:
        logging.critical(str(e))
        sys.exit(1)
