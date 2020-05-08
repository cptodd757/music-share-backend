from base64 import b64decode
import sys

sys.path.append('./route_helpers/func')
from hash_alg import hash_alg
from create_access_token import create_access_token
import db

def login_helper(request):
    creds = b64decode(request.headers['Authorization'])
    colon = creds.find(':')
    username, password_attempt = creds[:colon], creds[colon+1:]
    print(request.headers['Authorization'])
    
    user = db.find_one({"username":username})

    if user:
        pwa_hash = hash_alg(password_attempt)
        print('attempts:',username,password_attempt,pwa_hash)

        if user["password"].decode() == pwa_hash:
            return {'access_token':create_access_token(username),
                    'message':'Success!'}, 200
        else:
            return {'access_token':'',
                    'message':'Wrong password.'}, 202
    return {'access_token':'',
            'message':'User not found.'}, 404
