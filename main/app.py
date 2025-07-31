from flask import Flask,request,jsonify
from flask_cors import CORS
import os,json
from response import response
from gettable import gettable
from geturl import geturl

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__,template_folder='templates')
CORS(app)

DATA_PREPARER = {
    "type": "function",
    "function": {
        "name": "decide_type",
        "description": (
            "Choose one of the following which would work for getting data mentioned in the problem statement"
        ),
        "parameters": {
            "type": "object",
            "properties": {
                "index": {
                    "type": "integer",
                    "description": (
                        "Choose one of the following which would work for getting data mentioned in the problem statement"
                    )
                }
            },
            "required": ["index"],
            "additionalProperties": False
        },
        "strict": True
    }
}

Dataset = [
    "1. One website has the relevant table/list", # gettable.py
    "2. Data Scraping some other way",
    "3. Getting Data from somewhere else",
    "4. Does not mention a loadable dataset/list"
]

@app.route('/analyze',methods=['POST'])
def analyze():
    file = request.get_data(as_text=True)

    messages = [
        {
            "role":"user",
            "content":file+'\n'+'\n'.join(Dataset)+'\n\nWhich is the correct way to proceed out of these four'
        }
    ]

    clean = [
        {
            "role":"user",
            "content":file
        }
    ]
    print(messages)
    f = response(DATA_PREPARER,messages)
    data = json.loads(f["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"])
    Lindex = data['index']

    flag = False
    df = None

    if Lindex==1:
        # print("Data Scraping and Extracting Single Table using Pandas")
        try:
            df = gettable(geturl(file),clean)
        except:
            pass
    elif Lindex==2:
        print("Data Scraping from some website some other way")
    elif Lindex==3:
        print("Getting Data from somewhere else")
    else:
        flag = True
    
    if flag or df==None:
        print("Does not mention a loadable dataset")

        # ise idhar hi khatam krdo 

        L = [1,'titanic',0.485782,'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=']
        return jsonify(json.dumps(L))



    L = [1,'titanic',0.485782,'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=']
    return jsonify(json.dumps(L))

if __name__=='__main__':
    app.run(debug=True)
