from flask import Flask,request,jsonify
from flask_cors import CORS
import os,json
from response import response
# from gettable import gettable

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__,template_folder='templates')
CORS(app)

# DATA_PREPARER = {
#     "type": "function",
#     "function": {
#         "name": "extract_data",
#         "description": (
#             "Write complete code to load the dataset from the given URL or source, "
#             "without modifying, renaming, or assuming any column names. "
#             "Only include essential imports (like pandas) and the code to load the dataset. "
#             "Ensure the code runs correctly and stores the data in a variable."
#         ),
#         "parameters": {
#             "type": "object",
#             "properties": {
#                 "code": {
#                     "type": "string",
#                     "description": (
#                         "The complete code to load the dataset. Must include necessary imports, "
#                         "and store the loaded data in a variable (like df)."
#                     )
#                 },
#                 "data_type": {
#                     "type": "string",
#                     "description": "The data type of the variable storing the dataset (e.g., pandas.DataFrame)"
#                 }
#             },
#             "required": ["code", "data_type"],
#             "additionalProperties": False
#         },
#         "strict": True
#     }
# }

Dataset = [
    "1. Data Scraping and Extracting Single Table using Pandas", # gettable.py
    "2. Data Scraping from some website some Other Way",
    "3. Neither 1 nor 2" 
]

@app.route('/analyze',methods=['POST'])
def analyze():
    file = request.get_data(as_text=True)

    messages = [
        {
            "role":"user",
            "content":file
        }
    ]

    # else:
    #     for i in range(10):
    #         d = response(DATA_PREPARER,messages)
    #         d = json.loads(d["choices"][0]["message"]["tool_calls"][0]["function"]["arguments"])
    #         code,type1 = d["code"],d["data_type"]
    #         messages.append({"role":"agent","content":(d["code"],d["data_type"])})

    #         flag,output = isok(code,type1)
    #         finaloutput = output
    #         if flag:
    #             break
            

    #         print(code,type1)

    L = [1,'titanic',0.485782,'data:image/png;base64,iVBORw0KGgoAAAANSUhEUgAAAAEAAAABCAQAAAC1HAwCAAAAC0lEQVR4nGNgYAAAAAMAASsJTYQAAAAASUVORK5CYII=']
    return jsonify(json.dumps(L))

if __name__=='__main__':
    app.run(debug=True)
