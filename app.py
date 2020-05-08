from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
# from flask_bcrypt import Bcrypt
from base64 import b64decode
import json
import sys

sys.path.append('./route_helpers')
from login_helper import login_helper
from register_helper import register_helper

app = Flask(__name__)
CORS(app)
# bcrypt = Bcrypt(app)

@app.route('/',methods=['GET','POST'])
def index():
    return {'hello':'world'}

# TODO: Return 200 code and api token (in body of response) if username and password match
# Return 204 code if dont match
# return 404 (?) if user not found
@app.route('/api/login',methods=['GET','POST'])
def login():
    #print('request: ', b64decode(request.headers['Authorization']))
    ans = login_helper(request)#, bcrypt.generate_password_hash, bcrypt.check_password_hash)
    print(ans)
    return ans #{'login':'key'}, 200 #this works

@app.route('/api/register',methods=['GET','POST'])
def register():
    ans = register_helper(request)
    print(ans)
    return ans


if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)