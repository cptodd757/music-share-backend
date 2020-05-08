import jwt
import datetime

#placeholder. initialize as env variable upon setup
SECRET_KEY = '\xbc\x81\xa1\x07\xd1\xd5\r\xa1\xbc\xcaS\x1d\xdd\xc5\xd8\x87\x97V\x92\x00\x18.8\xbf'

def create_access_token(username): #todo: what params?
    payload = {
                'exp': datetime.datetime.utcnow() + datetime.timedelta(minutes=30),
                'iat': datetime.datetime.utcnow(),
                'sub': username
              }
    #placeholder secret key
    return jwt.encode(payload,
                      SECRET_KEY,#app.config.get('SECRET_KEY'),
                      algorithm='HS256')