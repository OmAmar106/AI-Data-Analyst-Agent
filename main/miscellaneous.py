from flask import Flask,request,jsonify
from flask_cors import CORS
import os,json
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from datetime import datetime

if 'VERCEL' in os.environ:
    from main.llm import AIPipeLLM
    from main.utils.main import listoftools
else:
    from llm import AIPipeLLM
    from utils.main import listoftools

llm = AIPipeLLM()
FORBIDDEN = ["shutil", "os", "subprocess", "open(", "rm", "rmtree", "remove", "unlink", "sys.exit", "exit("]

def safe_python_executor(code: str):
    if any(word in code for word in FORBIDDEN):
        return (
            "Your code contains unsafe operations like file deletion or system control. "
            "Please rewrite it **without using** any of these: "
            + ", ".join(FORBIDDEN)
        )
    return PythonREPLTool().run(code)

safe_tool = Tool(
    name="Safe Python Executor",
    func=safe_python_executor,
    description="Executes safe Python code for data analysis (e.g., pandas, matplotlib). Blocks file operations. You must not save any file to disk. You must do it within memory."
)

tools = [safe_tool]
# isme aur bahut kuch add krna hain 

system_prompt = (
    "You are a safe Python data analyst. Never use file deletion, OS commands, or subprocess. "
    "Avoid: " + ", ".join(FORBIDDEN)
)

agent = initialize_agent(
    tools=[safe_tool]+listoftools(),
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"system_message": system_prompt},
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
)


def ask_agent(message):
    return agent.run(
        message + "\n\n\nRespond with only the final answers, no explanation, no units. "
           "Each answer must be as short as possible and must be accurate, so make sure you do data cleaning properly."
           "Do NOT write full sentences. Also importantly, the output must be in the format specified in the given problem."
    )

# if __name__=='__main__':
#     t = agent.run(
#             open('test_cases/test_question.txt','r').read() + "\n\n\nRespond with only the final answers, no explanation, no units. "
#            "Each answer must be as short as possible and must be accurate, so make sure you do data cleaning properly."
#            "Do NOT write full sentences. Also importantly, the output must be in the format specified in the given problem."
#     )
#     print()
#     print(t)