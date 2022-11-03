import requests
from bs4 import BeautifulSoup as bs
from programs.vidstream import extract


class Anime:
    def __init__(self, url, img, lang, title, episode) -> None:
        self.url = url
        self.img = img
        self.lang = lang
        self.title = title
        self.episode = episode


class GoGoApi:
    def __init__(self) -> None:
        self.host = 'gogoanime.dk'

    def search(self, query, url_only=False):
        soup = bs(requests.get(
            f'https://{self.host}/search.html?keyword='+query).content, 'html.parser')
        div = soup.find('ul', 'items')
        animes = div.find_all('li')

        if url_only:
            results = []
            for i in animes:
                url = i.find('a').get('href').replace('/category/', '')
                results.append(url)
            return results

    def home(self):
        soup = bs(requests.get(
            f'https://{self.host}').content, 'html.parser')
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

    def get_episodes(self, anime):
        soup = bs(requests.get(
            f'https://{self.host}/category/{anime}').content, 'html.parser')

        ep = soup.find('a', 'active').get('ep_end')
        return int(ep.strip())

    def get_links(self, anime, episode):
        data = {}

        soup = bs(requests.get(
            f'https://{self.host}/{anime}-episode-{episode}').content, 'html.parser')
        div = soup.find('div', 'anime_muti_link')
        a = div.find_all('a')
        embeds = []

        for i in a:
            url = i.get('data-video')
            if not url.startswith('https'):
                url = 'https:'+url

            if 'gogohd' in url:
                url = extract(url)

            if 'mixdrop.co' in url:
                url = url.replace('mixdrop.co', 'mixdrop.ch')

            if 'mp4upload' not in url:
                embeds.append(url)

        if 'dub' in anime:
            data['DUB'] = embeds
        else:
            data['SUB'] = embeds
            anime += '-dub'

            soup = bs(requests.get(
                f'https://{self.host}/{anime}-episode-{episode}').content, 'html.parser')

            error = soup.find('h1', 'entry-title')
            if error:
                return data

            div = soup.find('div', 'anime_muti_link')
            a = div.find_all('a')
            embeds = []

            for i in a:
                url = i.get('data-video')
                if not url.startswith('https'):
                    url = 'https:'+url

                if 'gogohd' in url:
                    url = extract(url)

                if 'mixdrop.co' in url:
                    url = url.replace('mixdrop.co', 'mixdrop.ch')

                if 'mp4upload' not in url:
                    embeds.append(url)

            data['DUB'] = embeds
            return data