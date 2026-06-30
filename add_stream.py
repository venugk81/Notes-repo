import requests
from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="anything"  # Ollama ignores this
)


stream = client.chat.completions.create(
    model="gemma4:e2b",
    messages=[
        {"role": "user", "content": "what is credit risk?"}
    ],
    stream=True
)

for chunk in stream:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)
