from flask import Flask,request,jsonify
from flask_cors import CORS
import os,json
from llm import AIPipeLLM
from groq_client import Groq
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from datetime import datetime

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

system_prompt = (
    "You are a safe Python data analyst. Never use file deletion, OS commands, or subprocess. "
    "Avoid: " + ", ".join(FORBIDDEN)
)

agent = initialize_agent(
    tools=[safe_tool],
    llm=llm,
    agent=AgentType.STRUCTURED_CHAT_ZERO_SHOT_REACT_DESCRIPTION,
    verbose=True,
    agent_kwargs={"system_message": system_prompt},
    memory=ConversationBufferMemory(memory_key="chat_history", return_messages=True)
)


BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__,template_folder='templates')
CORS(app)

@app.route('/analyze',methods=['POST'])
def analyze():
    file = request.get_data(as_text=True)
    t = agent.run(
            file + "\n\n\nRespond with only the final answers, no explanation, no units. "
           "Each answer must be as short as possible."
           "Do NOT write full sentences."
    )

    # first categorize as data set is there or not

    isscraping = False
    return jsonify(json.dumps(t))

if __name__=='__main__':
    app.run(debug=True)
