import os

from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI(
    base_url="http://localhost:11434/v1",
    api_key="anything"  # Ollama ignores this
)

###giving multiple examples

SYSTEM_PROMPT = """
You are an expert AI assistant in resolving user questions using chain of thoughts.
You work on Start plan and output steps
you need to first plan what needs to be done. The plan can be multiple steps.
Once you think enough plan has been done, you can give an OUTPUT.

RULES:
    1. Before giving the final answer, produce a short plan.
    2. Return exactly one JSON object with either
    3. Only run one step at a time
    4. The sequence of steps is START (where user gives an input), PLAN that can be multiple steps, and 
    OUTPUT (where you give the final answer)

OUTPUT JSON Format:
    {"Step": "START" | "PLAN" | "OUTPUT", content: "string"}
Example:

    START: Hey, can you solve 2+3*5/2
    PLAN: {"Step": "PLAN", "content": "Seems like a simple arithmetic problem. I will solve it using BODMUS rules"}
    PLAN: {"Step": "PLAN", "content": "First I will solve the multiplication 3*5 = 15"}
    PLAN: {"Step": "PLAN", "content": "Second I will solve the multiplication 15/2 = 7.5"}
    PLAN: {"Step": "PLAN", "content": "Now finally I will solve the addition 2+7.5 = 9.5"}
    OUTPUT: {"Step": "OUTPUT", "content": "9.5"}}

"""

message_history = [{"role": "system", "content": SYSTEM_PROMPT}, ]
user_question = input("👉:")
message_history.append({"role": "user", "content": user_question})

while True:
    res = client.chat.completions.create(
        model="gemma4:e2b",
        response_format={"type": "json_object"},
        messages=message_history
    )

    raw_result = res.choices[0].message.content
    print(raw_result)

    parsed_result = json.loads(raw_result)

    message_history.append({
        "role": "assistant",
        "content": raw_result
    })

    step = parsed_result.get("Step")
    content = parsed_result.get("content")

    if step == "START":
        print("🔥", content)

    elif step == "PLAN":
        print("🧠", content)

    elif step == "OUTPUT":
        print("🤖", content)
        break

    else:
        print("Unexpected response:", parsed_result)
        break

# print(res.choices[0].message.content)

# this is for openai
# use the same, route to google api.

# {"role": "user", "content": "what is 2+2 ?"}      ##for this specific question, guardrail is placed.
# {"role": "user", "content": "hi gemini how are you ?"}
