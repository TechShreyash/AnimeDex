import requests


def update_views(anime):
    try:
        requests.get(
            'https://animedex-api.vercel.app/db/save?anime='+anime.strip())
    except:
        pass
    return
