from json import loads

import sys
sys.path.append('./route_helpers/func')
from authorize import authorize
import db

# TODO: friend REQUESTS, not just auto-add
# request["Authorization"] will be Bearer <access_token>
def add_friend_helper(request):
    # check access token
    user = authorize(request)
    if not user:
        return {"message":"Not authorized!"}, 401

    # check to see that desired friend exists
    friend_username = loads(request.data)["friend_username"]
    if not db.find_one({"username":friend_username}):
        return {"message":"Friend does not exist"}, 404

    # check that friend isnt already in friend's list
    if db.find_one({"username":user,"friends":{"$elemMatch": {"username":friend_username}}}):
        return {"message":"Already friends with this user"}, 202

    # check that friend isnt already in friend's request list
    if db.find_one({"username":user,"friend_requests":friend_username}):
        return {"message":"This friend is waiting for you to accept their request!"}, 202

    # # add desired friend to user's friend list
    # friends = db.find_one({"username":user})["friends"]
    # new_friend = {"username":friend_username,
    #               "songsReceived":[],
    #               "songsSent":[]}
    # friends.append(new_friend) 
    # db.update_one({"username":user},{"$set":{"friends":friends}})

    # NEW 5/12/20: add user to other friend's friend REQUESTS list
    # add user to the other friend's friend list
    other_friends = db.find_one({"username":friend_username})["friend_requests"]
    other_friends.append(user)#,
                        #   "songsReceived":[],
                        #   "songsSent":[]})
    db.update_one({"username":friend_username},{"$set":{"friend_requests":other_friends}})
    
    return {"message":"friend requested!"}, 200