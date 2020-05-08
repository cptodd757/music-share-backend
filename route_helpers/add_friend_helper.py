from json import loads

import sys
sys.path.append('./route_helpers/func')
from authorize import authorize
import db

# request["Authorization"] will be Bearer <access_token>
def add_friend_helper(request):
    user = authorize(request)
    if not user:
        return {"message":"Not authorized!"}, 401

    friend_username = loads(request.data)["friend_username"]
    if not db.find_one({"username":friend_username}):
        return {"message":"Friend does not exist"}, 404
        
    query = {"username":user}
    friends = db.find_one(query)["friends"]
    new_friend = {"username":friend_username,
                  "songs":[]}
    friends.append(new_friend) 
    db.update_one(query,{"$set":{"friends":friends}})
    
    return {"message":"friend added!"}, 200