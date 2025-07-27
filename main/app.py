from flask import Flask
from flask_cors import CORS
import os

BASE_DIR = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
app = Flask(__name__,template_folder='templates')
CORS(app)

@app.route('/analyze',methods=['POST'])
def analyze():
    pass

if __name__=='__main__':
    app.run(debug=True)

