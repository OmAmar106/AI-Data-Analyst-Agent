from flask import request
from response import response
import json

SCRAPER_TOOL = {
    "type": "function",
    "function": {
        "name": "extract_url",
        "description": "Extract the website link or URL that needs to be scraped from the input text",
        "parameters": {
            "type": "object",
            "properties": {
                "url": {
                    "type": "string",
                    "description": "The full URL that the problem statement, that is user asks for to be scraped (e.g. https://example.com/page)"
                }
            },
            "required": ["url"],
            "additionalProperties": False
        },
        "strict": True
    }
}

def geturl(file):

    messages = [
        {
            "role":"user",
            "content":file
        }
    ]

    d = response(SCRAPER_TOOL,messages)
    url = json.loads(d["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"])["url"]

    return url

if __name__=="__main__":
    print(geturl(open("test_cases/test_question.txt","r").read()))