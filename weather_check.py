import os
from pickletools import string1
from pyexpat.errors import messages

import requests
from dotenv import load_dotenv

from openai import OpenAI

'''
Google AI Studio Configuration (Public/Developer)If you are using Google AI Studio keys, 
configure your OpenAI client with these specific environment variables or initialization
 values:Base URL: https://generativelanguage.googleapis.com/v1beta/openai/

 ##api_key= is google api key - https://aistudio.google.com/
## base_url- calls are redirected to google instead of open ai
## we are doing this because open ai is a paid tool and trainer is using open ai for training
##since we are not buying the tokens, we will use gemini and use the same syntax as trainer.

'''
load_dotenv()

client = OpenAI(
    api_key= f"{os.getenv('GOOGLE_API_KEY')}",
    base_url = "https://generativelanguage.googleapis.com/v1beta"
)
# https://wttr.in/tamilnadu?format=%C+%t

def get_weather(city):

    url = f"https://wttr.in/{city.lower()}?format=%C+%t"
    response = requests.get(url)
    if response.status_code != 200:
        return f"Something went wrong- response status code: {response.status_code}"
    return response.text

def main():
    user_query=input("Enter your query: >> ")
    res = client.chat.completions.create(
        model = "gemini-2.5-flash",
        messages=[{"role" :"user", "content": user_query}]
    )
    response = res.choices[0].message.content
    print(response)
    return response



main()
