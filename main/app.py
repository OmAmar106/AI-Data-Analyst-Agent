from flask import Flask,request,jsonify
from flask_cors import CORS
import os,json
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
app = Flask(__name__,template_folder='templates')
CORS(app)

@app.route('/analyze',methods=['POST'])
def analyze():
    file = request.get_data(as_text=True)
    # t = agent.run(
    #         file + "\n\n\nRespond with only the final answers, no explanation, no units. "
    #        "Each answer must be as short as possible."
    #        "Do NOT write full sentences."
    # )

    # first categorize as data set is there or not

    # 1st -> groq else langchain

    output = None

    try:
        output = Groq.run(file)
        if not output:
            assert(False)
    except:
        try:
            output = ask_agent(file)
        except:
            pass

    f_output = format(file,output)

    return jsonify(json.dumps(f_output))

if __name__=='__main__':
    app.run(host="0.0.0.0", port=5000)
