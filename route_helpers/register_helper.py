from base64 import b64decode

import sys
sys.path.append('./route_helpers/func')
from hash_alg import hash_alg
from create_access_token import create_access_token
import db

# if user already exists, return 202
# if user does not already exist, return 200 and an access token
def register_helper(request):
    creds = b64decode(request.headers['Authorization'])
    colon = creds.find(':')
    username, password = creds[:colon], creds[colon+1:]
    print(request.headers['Authorization'])

    if db.find_one({"username":username}):
        return {'access_token':'',
                    'message':'User already exists. Please login.'}, 202
    
    # user doesn't already exist
    db.insert_one({"username":username,
                   "password":hash_alg(password).encode(),
                   "friends":[]})

    return {'access_token':create_access_token(username),
                    'message':'Account created!'}, 200