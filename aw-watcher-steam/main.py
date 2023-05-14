import requests
from datetime import datetime, timedelta, timezone
from time import sleep

from aw_core.models import Event
import logging
from aw_client import ActivityWatchClient




def get_currently_played_game():
    api_key = ""
    steam_id = "76561198333678249"
    url = f"http://api.steampowered.com/ISteamUser/GetPlayerSummaries/v0002/?key={api_key}&steamids={steam_id}"
    reponse = requests.get(url=url)
    data = {}
    if reponse.status_code == 200: 
        data = reponse.json()["response"]["players"][0]
        if "gameextrainfo" in data: 
            return data["gameextrainfo"]
    return None


if __name__ == "__main__": 
    client = ActivityWatchClient("aw-watcher-steam", testing=True)
    bucket_name = "{}_{}".format(client.client_name, client.client_hostname)    
    client.create_bucket(bucket_name, event_type="currently-playing-game")
    client.connect()

    while True:
        game = get_currently_played_game()
        if game != None: 
            now = datetime.now(timezone.utc)
            data = {"currently-played-game": game}
            event = Event(timestamp=now, data = data)
            client.heartbeat(bucket_name, event= event, pulsetime= 7, queued=True, commit_interval=4)
            print(f"Playing {game}")
        else: 
            print("not playing")
        sleep(5)
    
    