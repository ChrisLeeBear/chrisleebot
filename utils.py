# utils.py
# A bunch of utility functions

import cfg
import urllib3, json
import time, threading
from time import sleep
from twitchobserver import Observer as obs



# Function: threadFillOpList
# In a separate thread, fill up the op list
def threadFillOpList():
    while True:
        try:
            url = "http://tmi.twitch.tv/group/user/chris_lee_bear/chatters"
            req = urllib3.PoolManager(maxsize=10).request('GET',url, headers={"accept": "*/*"})
            response = urllib3.PoolManager(maxsize=10).urlopen(req).read()
            if response.find("502 Bad Gateway") == -1:
                cfg.oplist.clear()
                data = json.loads(response)
                for p in data["chatters"]["moderators"]:
                    cfg.oplist[p] = "mod"
                for p in data["chatters"]["global_mods"]:
                    cfg.oplist[p] = "global_mod"
                for p in data["chatters"]["admins"]:
                    cfg.oplist[p] = "admin"
                for p in data["chatters"]["staff"]:
                    cfg.oplist[p] = "staff"
        except:
            'do nothing'
        sleep(5)

def isOp(user):
    return user in cfg.oplist