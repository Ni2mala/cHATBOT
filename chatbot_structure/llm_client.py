# llm_client.py

import requests
from config import OLLAMA_URL, MODEL_NAME, REQUEST_TIMEOUT

def call_llm(messages):
    try:
        response = requests.post(
            OLLAMA_URL,
            json={
                "model": MODEL_NAME,
                "messages": messages,
                "stream": False
            },
            timeout=REQUEST_TIMEOUT
        )

        response.raise_for_status()
        data = response.json()

        return data["message"]["content"]

    except requests.exceptions.RequestException as e:
        return f"[ERROR] LLM request failed: {e}"

    except (KeyError, ValueError):
        return "[ERROR] Invalid response from LLM"
