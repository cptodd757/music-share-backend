from json import loads

import sys
sys.path.append('./route_helpers/func')
from authorize import authorize
import db

def accept_friend_request_helper(request):
    # check access token
    user = authorize(request)
    if not user:
        return {"message":"Not authorized!"}, 401

    body = loads(request.data)
    friend_username = body["friend_username"]
    
    if not db.find_one({"username":user,"friend_requests": friend_username}):
        return {"message":"Friend not found in pending friend requests.  Weird"}, 404

    # add accepted friend to user's friend list
    friends = db.find_one({"username":user})["friends"]
    new_friend = {"username":friend_username,
                  "songsReceived":[],
                  "songsSent":[]}
    friends.append(new_friend) 
    db.update_one({"username":user},{"$set":{"friends":friends}})

    # clear new friend from requests
    db.update_one({"username":user},{"$pull":{"friend_requests":friend_username}})

    # add user to the accepted friend's friend list
    other_friends = db.find_one({"username":friend_username})["friends"]
    other_friends.append({"username":user,
                          "songsReceived":[],
                          "songsSent":[]})
    db.update_one({"username":friend_username},{"$set":{"friends":other_friends}})

    return {"message":"friend added!"}, 200