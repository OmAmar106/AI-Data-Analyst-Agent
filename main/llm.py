from langchain_core.language_models.llms import LLM
from typing import Optional, List
import requests
import os
from dotenv import load_dotenv
import random

load_dotenv()

key = os.getenv('AI_PIPE_API_KEY')
key1 = os.getenv('AI_PIPE_API_KEY1')
key2 = os.getenv('AI_PIPE_API_KEY2')
key3 = os.getenv('AI_PIPE_API_KEY3')
key4 = os.getenv('AI_PIPE_API_KEY4')
pkey = os.getenv('PERPLEXITY_API_KEY')

keys = [pkey,key,key1,key2,key3,key4]

class AIPipeLLM(LLM):
    # api_url: str = "https://aipipe.org/openrouter/v1/chat/completions"
    api_url: str = "https://api.perplexity.ai/chat/completions"
    api_key: Optional[str] = None

    @property
    def _llm_type(self) -> str:
        return "aipipe"
    
    def _call(self, prompt: str, stop: Optional[List[str]] = None, **kwargs) -> str:
        for i in range(5):
            # randomnum = random.randint(0,4)
            randomnum = 0
            key = keys[randomnum]
            try:
                headers = {
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "sonar-pro",
                    "messages": [{"role": "user", "content": prompt}]
                }

                response = requests.post(self.api_url, headers=headers, json=payload)
                return response.json()['choices'][0]['message']['content']
            except:
                pass
        return None
    
    def invoke(self,prompt,stop=None):
        for i in range(5):
            # randomnum = random.randint(0,4)
            randomnum = 0
            key = keys[randomnum]
            try:
                headers = {
                    "Authorization": f"Bearer {key}",
                    "Content-Type": "application/json"
                }
                payload = {
                    "model": "openai/gpt-3.5-turbo",
                    "messages": [{"role": "user", "content": prompt}]
                }

                response = requests.post(self.api_url, headers=headers, json=payload)
                return response.json()['choices'][0]['message']['content']
            except:
                pass
        return None

if __name__=='__main__':
    templlm = AIPipeLLM()
    print(templlm.invoke("What is the capital of India?"))
