import jwt

#placeholder. initialize as env variable upon setup
SECRET_KEY = '\xbc\x81\xa1\x07\xd1\xd5\r\xa1\xbc\xcaS\x1d\xdd\xc5\xd8\x87\x97V\x92\x00\x18.8\xbf'

# return false whenever something no bueno happens
def authorize(request):
    auth = ''
    try:
        auth = request.headers["Authorization"]
        index = auth.find("Bearer")
    except Exception:
        print("no bearer auth")
        return False

    access_token = auth.split(" ")[1]
    print('access_token',access_token)

    try:
        payload = jwt.decode(access_token, SECRET_KEY)#app.config.get('SECRET_KEY'))
        user = payload['sub']
        print(user)
        return user 
    except jwt.ExpiredSignatureError:
        print('expired token')
        return False
    except jwt.InvalidTokenError:
        print('invalid token')
        return False