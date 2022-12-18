import requests
from bs4 import BeautifulSoup as bs

ANIME_POS = """
<a href="{}"><div class="poster la-anime">
                    <div id="shadow1" class="shadow">
                            <div class="dubb">{}</div>
                            <div class="dubb dubb2">{}</div>
                        </div>
                        <div id="shadow2" class="shadow">
                        <img class="lzy_img" src="https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/img/loading.gif" data-src="{}">
                    </div>
                    <div class="la-details">
                        <h3>{}</h3>
                        <div id="extra">
                        <span>{}</span>
                        <span class="dot"></span>
                        <span>{}</span>                        
                        </div>
                    </div>
                </div></a>
"""


class Anime:
    def __init__(self, url, img, lang, title, episode) -> None:
        self.url = url
        self.img = img
        self.lang = lang
        self.title = title
        self.episode = episode


def get_GPage(page):
    url = f'https://gogoanime.bid/?page={str(page)}'
    soup = bs(requests.get(url).content, 'html.parser')
    div = soup.find('ul', 'items')
    animes = div.find_all('li')
    results = []
    for i in animes:
        url = '/anime' + \
            i.find('a').get('href').replace(
                '/category/', '').split('-episode-')[0]
        img = i.find('img').get('src')
        lang = i.find('div', 'type').get('class')[1].replace('ic-', '')
        title = i.find('a').get('title')
        episode = i.find('p', 'episode').text.replace('Episode', '')
        results.append(
            Anime(url, img, lang, title, episode)
        )
    return results


def get_html(data):
    html = ''

    for i in data:
        i: Anime

        x = ANIME_POS.format(
            i.url,
            i.lang,
            'Ep '+str(i.episode).strip(),
            i.img,
            i.title,
            f'Latest {i.lang}',
            'HD'
        )
        html += x

    return html
