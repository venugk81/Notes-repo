

import requests
from dotenv import load_dotenv

from openai import OpenAI


load_dotenv()

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="anything"  # Ollama ignores this
)



def get_weather(city):

    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    print(response.text)
    if response.status_code != 200:
        return f"Something went wrong- response status code: {response.status_code}"
    return response.text

def main():
    user_query=input("Enter your query: >> ")
    res = client.chat.completions.create(
        model = "gemma4:e2b",
        messages=[{"role" :"user", "content": user_query}],
        max_tokens=300,

    )
    response = res.choices[0].message.content
    print(response)

    return response



main()
get_weather("Delhi")


'''
Open WebUI
      ↓
OpenAI-compatible API
      ↓
Ollama
      ↓
gemma4:2b

then there are no OpenAI-style token quotas. The client simply forwards your prompt to Ollama.
The only time you'll hit a limit is when:
the prompt exceeds the configured context length,
your machine runs out of RAM/VRAM,
or the application itself imposes its own maximum input size.

   max_tokens=300
   
This is not a quota—it's simply a limit for that response.


'''
