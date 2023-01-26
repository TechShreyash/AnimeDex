import requests


def update_views(anime):
    try:
        requests.get(
            'https://api.animedex.live/db/view?anime='+anime.strip())
    except:
        pass
    return


def update_watch(anime):
    try:
        requests.get(
            'https://api.animedex.live/db/watch?anime='+anime.strip())
    except:
        pass
    return
