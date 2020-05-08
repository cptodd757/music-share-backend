import jwt
import datetime
from base64 import b64decode
from flask import make_response
import hashlib
import os
import pymongo
from login_helper import create_access_token

import sys
sys.path.append('./route_helpers/func')
from hash_alg import hash_alg

# if user already exists, return 202
# if user does not already exist, return 200 and an access token
def register_helper(request):
    creds = b64decode(request.headers['Authorization'])
    colon = creds.find(':')
    username, password = creds[:colon], creds[colon+1:]
    print(request.headers['Authorization'])

    if user_exists(username):
        return {'access_token':'',
                    'message':'User already exists. Please login.'}, 202
    
    # user doesn't exist

    #salt = os.urandom(32)
    full_pw_hash = hash_alg(password)#, salt)
    #full_pw_hash = salt + pw_hash

    #TODO: create a db.py file that handles all interfacing with mongodb
    client = pymongo.MongoClient('localhost', 27017)
    db = client["music_share"]
    users = db["users"]

    users.insert_one({"username":username,"password":full_pw_hash.encode()})

    return {'access_token':create_access_token(username),
                    'message':'Account created!'}, 200

def user_exists(username):
    client = pymongo.MongoClient('localhost', 27017)
    db = client["music_share"]
    users = db["users"]

    user = users.find_one({"username":username})
    if user is None:
        return False
    return True

# def hash_alg(password, salt):
#     return hashlib.pbkdf2_hmac('sha256',
#                                 password.encode('utf-8'), # Convert the password to bytes
#                                 salt, 
#                                 100000)