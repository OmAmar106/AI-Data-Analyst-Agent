import requests
import os
from dotenv import load_dotenv

load_dotenv()

url = "https://aipipe.org/openrouter/v1/chat/completions"
headers = {
    "Authorization": f"Bearer {os.getenv('AI_PIPE_API_KEY')}",
    "Content-Type": "application/json"
}

def hashcustom(d):
    return d["function"]["name"]

dp = {}
def response(function,message):
    if (hashcustom(function),message[0]["content"]) in dp:
        return dp[(hashcustom(function),message[0]["content"])]
    payload = {
        "model": "openai/gpt-3.5-turbo",
        "messages": message,
        "tools":[function],
        "tool_choice": "auto"
    }


    response = requests.post(url, headers=headers, json=payload)
    dp[(hashcustom(function),message[0]["content"])] = response
    return response.json()