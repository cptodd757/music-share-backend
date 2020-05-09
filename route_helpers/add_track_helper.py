import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
from json import loads
import datetime

import sys
sys.path.append('./route_helpers/func')
from authorize import authorize
import db
import config

sp = spotipy.Spotify(client_credentials_manager=SpotifyClientCredentials(client_id=config.CLIENT_ID,client_secret=config.CLIENT_SECRET))

def add_track_helper(request):
    user = authorize(request)
    if not user:
        return {"message":"Not authorized!"}, 401

    body = loads(request.data)
    track_id = body["track_url"]
    try:
        track_id = track_id.split("track/")[1]
    except Exception:
        print("excepted something")
        print(track_id)

    try:
        track = sp.track(track_id)

        entry = {}
        entry["note"] = body["note"]

        entry["title"] = track["name"]
        entry["artist"] = ', '.join([artist["name"] for artist in track["artists"]])
        entry["album"] = track["album"]["name"]
        #entry["release_date"]
        #entry["duration"]
        entry["id"] = track["id"]
        #entry["noteworthy_timestamp"]
        entry["date_added"] = datetime.datetime.utcnow()

        # songlist = db.find_one({"username":body["friend_username"]})["songs"]
        # songlist.append(entry)

        db.update_one({"username": body["friend_username"], "friends.username": user},
        { "$push": 
            {"friends.$.songs": 
                entry
            }
        })
        return {"message":"Song added!"}, 200
    except Exception:
        return {"message":"Something went wrong"},500

    
    
