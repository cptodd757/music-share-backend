import bcrypt

#TODO: store salt and hash instead of using same salt everytime
def hash_alg(password):
    salt = '$2b$12$GkXDQQIQM7uLIXO4GhV3he'
    return bcrypt.hashpw(password, salt)