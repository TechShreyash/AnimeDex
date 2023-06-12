import requests
from bs4 import BeautifulSoup as bs

ANIME_POS = """<a href="{}"><div class="poster la-anime"> <div id="shadow1" class="shadow"> <div class="dubb">{}</div> <div class="dubb dubb2">{}</div> </div> <div id="shadow2" class="shadow"> <img class="lzy_img" src="https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/img/loading.gif" data-src="{}"> </div> <div class="la-details"> <h3>{}</h3> <div id="extra"> <span>{}</span> <span class="dot"></span> <span>{}</span> </div> </div> </div></a>"""


class Anime:
    def __init__(self, url, img, lang, title, episode) -> None:
        self.url = url
        self.img = img
        self.lang = lang
        self.title = title
        self.episode = episode
