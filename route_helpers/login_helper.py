import jwt
import datetime
from base64 import b64decode
from flask import make_response
import hashlib
import os
import sys
import pymongo

sys.path.append('./route_helpers/func')
from hash_alg import hash_alg

# Should return:
# body {"access_token: <>"}, <200|204|404>

# look for user in db
# if there, verify pw (else return 404)
# if pw right, return access token
# else say wrong pw
def login_helper(request):#, encode_alg, decode_alg):
    creds = b64decode(request.headers['Authorization'])
    colon = creds.find(':')
    username, password_attempt = creds[:colon], creds[colon+1:]
    print(request.headers['Authorization'])
    

    correct_pw = get_pw(username)

    if correct_pw is not None:
        pwa_hash = hash_alg(password_attempt)#, correct_pw[:32])
        print('attempts:',username,password_attempt,pwa_hash)
        #correct_pw = correct_pw[32:]
        print('correct password:',correct_pw)
        if correct_pw == pwa_hash:
            return {'access_token':create_access_token(username),
                    'message':'Success!'}, 200
        else:
            return {'access_token':'',
                    'message':'Wrong password.'}, 202
    return {'access_token':'',
            'message':'User not found.'}, 404

#return None if user no exist
def get_pw(username):
    client = pymongo.MongoClient('localhost', 27017)
    db = client["music_share"]
    users = db["users"]

    user = users.find_one({"username":username})
    if user is None:
        return None
    return user["password"].decode()
    # salt, password

    #return 'true_hashed_password','asdfasdfasdfasdfasdfasdfasdfasdf'

def create_access_token(username): #todo: what params?
    payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                'iat': datetime.datetime.utcnow(),
                'sub': username
              }
    #placeholder secret key
    return jwt.encode(payload,
                      '\xbc\x81\xa1\x07\xd1\xd5\r\xa1\xbc\xcaS\x1d\xdd\xc5\xd8\x87\x97V\x92\x00\x18.8\xbf',#app.config.get('SECRET_KEY'),
                      algorithm='HS256')

# def hash_alg(password_attempt, salt):
#     return hashlib.pbkdf2_hmac('sha256',
#                                 password_attempt.encode('utf-8'), # Convert the password to bytes
#                                 salt, 
#                                 100000)

