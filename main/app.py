from flask import Flask, request, jsonify
from flask_cors import CORS
import os, json, base64, requests
from langchain.agents import initialize_agent, AgentType
from langchain_experimental.tools.python.tool import PythonREPLTool
from langchain.agents import Tool
from langchain.memory import ConversationBufferMemory
from datetime import datetime

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
app = Flask(__name__, template_folder='templates')
CORS(app)

def upload_to_transfersh(file_bytes, filename):
    url = f"https://transfer.sh/{filename}"
    resp = requests.put(url, data=file_bytes)
    if resp.status_code == 200:
        return resp.text.strip()
    else:
        raise Exception(f"Upload failed: {resp.status_code} - {resp.text}")

@app.route('/analyze', methods=['POST'])
def analyze():
    uploaded_files = request.files
    statement_text = ""
    images_b64 = []
    dataset_url = None

    for filename, file_storage in uploaded_files.items():
        ext = filename.lower()
        data = file_storage.read()

        if ext.endswith(('.txt', '.md')):
            statement_text += data.decode('utf-8', errors='ignore') + "\n"

        elif ext.endswith(('.png', '.jpg', '.jpeg', '.gif')):
            b64_str = base64.b64encode(data).decode('utf-8')
            images_b64.append(f"data:image/{ext.split('.')[-1]};base64,{b64_str}")

        elif ext.endswith(('.csv', '.xlsx')):
            try:
                dataset_url = upload_to_transfersh(data, filename)
            except Exception as e:
                dataset_url = f"[Error uploading dataset: {e}]"

    output = None

    if statement_text and images_b64 and not dataset_url:
        combined_input = statement_text + "\n\nAttached Images:\n" + "\n".join(images_b64)
        try:
            output = Groq.run(combined_input)
        except:
            output = ask_agent(combined_input)
    elif dataset_url and images_b64:
        combined_input = statement_text + f"\n\nDataset available at: {dataset_url}" + "\n\nAttached Images:\n" + "\n".join(images_b64)
        try:
            output = Groq.run(combined_input)
        except:
            output = ask_agent(combined_input)
    elif dataset_url:
        combined_input = statement_text + f"\n\nDataset available at: {dataset_url}"
        try:
            output = Groq.run(combined_input)
        except:
            output = ask_agent(combined_input)
    else:
        try:
            output = Groq.run(statement_text)
        except:
            output = ask_agent(statement_text)

    f_output = format(statement_text, output)
    return f_output

if __name__ == '__main__':
    app.run(host="0.0.0.0", port=5000)
