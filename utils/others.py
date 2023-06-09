import random
import requests


def get_atitle(title):
    if not title:
        return "Unknown"

    tit = title.get("english")
    if not tit:
        tit = title.get("romaji")
        if not tit:
            tit = title.get("native")
    return tit


def get_other_title(title):
    if not title:
        return "Unknown"
    other = ""
    tit = title.get("english")
    if tit:
        other += tit + ", "
    tit = title.get("romaji")
    if tit:
        other += tit + ", "
    tit = title.get("native")
    if tit:
        other += tit + ", "
    return tit[:-2]


def get_studios(stud):
    tit = ""
    for i in stud:
        tit += i.get("name") + ", "
    return tit[:-2]


def get_genre(genres):
    if not genres or len(genres) == 0:
        return ""
    return random.choice(genres)


def get_urls(title):
    return "/anime/" + str(requests.utils.quote(title))


def get_t_from_u(url):
    return str(requests.utils.unquote(url)).replace("/anime/", "")
