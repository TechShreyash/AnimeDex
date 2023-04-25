import requests
from config import API_KEY


def update_views(anime):
    try:
        requests.get(
            f"https://api.animedex.live/db/view?key={API_KEY}&anime={anime.strip()}"
        )
    except Exception as e:
        print(e)
    return


def update_watch(anime):
    try:
        requests.get(
            f"https://api.animedex.live/db/watch?key={API_KEY}&anime={anime.strip()}"
        )
    except Exception as e:
        print(e)
    return
