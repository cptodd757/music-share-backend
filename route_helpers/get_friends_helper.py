import sys
sys.path.append('./route_helpers/func')
from authorize import authorize
import db

def get_friends_helper(request):
    user = authorize(request)
    if not user:
        return {"message":"Not authorized!"}, 401

    user_entry = db.find_one({"username":user})#["friends"]
    return {"friends":user_entry["friends"],"friend_requests":user_entry["friend_requests"]}, 200