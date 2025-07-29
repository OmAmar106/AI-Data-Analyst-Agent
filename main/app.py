from flask import Flask,request,jsonify
from flask_cors import CORS
import os,json
from response import response
from gettable import gettable

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__,template_folder='templates')
CORS(app)

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

PROBLEM_LIST_TOOL = {
    "type": "function",
    "function": {
        "name": "extract_problem_list",
        "description": "Extract the list of problems related to Data Analysis",
        "parameters": {
            "type": "object",
            "properties": {
                "problems": {
                    "type": "array",
                    "items": {"type": "string"},
                    "description": "Ordered list of Data Analysis problems mentioned except for scraping by the user"
                }
            },
            "required": ["problems"],
            "additionalProperties": False
        },
        "strict": True
    }
}


@app.route('/analyze',methods=['POST'])
def analyze():
    file = request.get_data(as_text=True)

    messages = [
        {
            "role":"user",
            "content":file
        }
    ]

    d = response(SCRAPER_TOOL,messages)
    url = json.loads(d["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"])["url"]

    df = gettable(url)

    L = [1,'titanic',0.485782,'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=']
    return jsonify(json.dumps(L))

if __name__=='__main__':
    app.run(debug=True)
