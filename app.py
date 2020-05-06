from flask import Flask, jsonify, redirect, request
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/',methods=['GET','POST'])
def index():
    return {'hello':'world'}


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)