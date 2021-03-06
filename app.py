from flask import Flask, jsonify, redirect, request
from flask_cors import CORS
import json
import sys

sys.path.append('./route_helpers')
from login_helper import login_helper
from register_helper import register_helper
from add_friend_helper import add_friend_helper
from add_track_helper import add_track_helper
from get_friends_helper import get_friends_helper
from accept_friend_request_helper import accept_friend_request_helper

app = Flask(__name__)
CORS(app)

@app.route('/api/login',methods=['GET','POST'])
def login():
    ans = login_helper(request)
    print(ans)
    return ans

@app.route('/api/register',methods=['GET','POST'])
def register():
    ans = register_helper(request)
    print(ans)
    return ans

@app.route('/api/add_friend',methods=['GET','POST'])
def add_friend():
    ans = add_friend_helper(request)
    print(ans)
    return ans

@app.route('/api/add_track',methods=['GET','POST'])
def add_track():
    ans = add_track_helper(request)
    print(ans)
    return ans

@app.route('/api/get_friends',methods=['GET'])
def get_friends():
    ans = get_friends_helper(request)
    print(ans)
    return ans

@app.route('/api/accept_friend_request',methods=['GET','POST'])
def accept_friend_request():
    ans = accept_friend_request_helper(request)
    print(ans)
    return ans

if __name__ == '__main__':
    app.run(host='0.0.0.0',port=4000)