from flask import Flask,request,jsonify
from flask_cors import CORS
import os,json
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from datetime import datetime
import base64

if 'VERCEL' in os.environ:
    from main.groq_client import Groq
    from main.formatter import format
    from main.miscellaneous import ask_agent
    from main.utils.main import listoftools
else:
    from groq_client import Groq
    from formatter import format
    from miscellaneous import ask_agent
    from utils.main import listoftools

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__,template_folder='templates')
CORS(app)

@app.route('/analyze', methods=['POST'])
def analyze():
    uploaded_files = request.files
    statement_text = ""
    images_b64 = []
    dataset_path = None

    for filename, file_storage in uploaded_files.items():
        ext = filename.lower()
        data = file_storage.read()

        if ext.endswith(('.txt', '.md')):
            statement_text += data.decode('utf-8', errors='ignore') + "\n"

        elif ext.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            b64_str = base64.b64encode(data).decode('utf-8')
            images_b64.append(f"data:image/{ext.split('.')[-1]};base64,{b64_str}")

        elif ext.endswith(('.csv', '.xlsx')):
            dataset_path = os.path.join(BASE_DIR, 'uploaded_' + filename)
            with open(dataset_path, 'wb') as f:
                f.write(data)

    output = None

    if statement_text and images_b64 and not dataset_path:
        combined_input = statement_text + "\n\nAttached Images:\n" + "\n".join(images_b64)
        try:
            output = Groq.run(combined_input)
        except:
            output = ask_agent(combined_input)
    elif dataset_path:
        combined_input = statement_text + f"\n\nDataset saved at: {dataset_path}"
        try:
            output = ask_agent(combined_input)
        except:
            output = Groq.run(combined_input)
    else:
        try:
            output = Groq.run(statement_text)
        except:
            output = ask_agent(statement_text)

    f_output = format(statement_text, output)
    return f_output

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
