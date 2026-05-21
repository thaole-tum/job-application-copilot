import requests
import os
from dotenv import load_dotenv


load_dotenv()

def call_llm(prompt: str):
    ollama_host = os.getenv("OLLAMA_HOST", "http://localhost:11434").rstrip("/")
    model_name = os.getenv("LLM_MODEL", "llama3")
    timeout_seconds = int(os.getenv("LLM_TIMEOUT", "300"))
    response = requests.post(
        f"{ollama_host}/api/generate",
        json={
            "model": model_name,
            "prompt": prompt,
            "stream": False
        },
        timeout=timeout_seconds,
    )
    response.raise_for_status()
    data = response.json()
    if "response" not in data:
        raise ValueError(f"Unexpected LLM response shape: {data}")
    return data["response"]
