from json import loads

import sys
sys.path.append('./route_helpers/func')
from authorize import authorize
import db

# TODO: friend REQUESTS, not just auto-add
# request["Authorization"] will be Bearer <access_token>
def add_friend_helper(request):
    user = authorize(request)
    if not user:
        return {"message":"Not authorized!"}, 401

    friend_username = loads(request.data)["friend_username"]
    if not db.find_one({"username":friend_username}):
        return {"message":"Friend does not exist"}, 404

    # add desired friend to user's friend list
    friends = db.find_one({"username":user})["friends"]
    new_friend = {"username":friend_username,
                  "songs":[]}
    friends.append(new_friend) 
    db.update_one({"username":user},{"$set":{"friends":friends}})

    # add user to the other friend's friend list
    other_friends = db.find_one({"username":friend_username})["friends"]
    other_friends.append({"username":user,
                          "songs":[]})
    db.update_one({"username":friend_username},{"$set":{"friends":other_friends}})
    
    return {"message":"friend added!"}, 200