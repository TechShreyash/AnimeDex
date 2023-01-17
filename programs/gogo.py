import requests
from bs4 import BeautifulSoup as bs


class Anime:
    def __init__(self, url, img, lang, title, episode) -> None:
        self.url = url
        self.img = img
        self.lang = lang
        self.title = title
        self.episode = episode


class GoGoApi:
    def __init__(self) -> None:
        self.host = 'gogoanime.bid'

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
        else:
            results = []
            for i in animes:
                url = i.find('a').get('href').replace('/category/', '')
                img = i.find('img').get('src')
                title = i.find('p', 'name').text
                released = i.find('p', 'released').text
                results.append(
                    Anime(url, img, released, title, None)
                )
            return results

    def anime(self, anime):
        soup = bs(requests.get(
            f'https://{self.host}/category/'+anime).content, 'html.parser')

        if soup.find('title').text == "Pages not found":
            return 'Error'

        title = soup.find('h1').text
        types = soup.find_all('p', 'type')
        try:
            synopsis = types[1].text.replace('Plot Summary: ', '').strip()
        except:
            synopsis = '?'
        try:
            names = types[5].text.replace('Other name: ', '').strip()
        except:
            names = '?'
        studios = '?'
        try:
            ep = soup.find('a', 'active').get('ep_end')
        except:
            ep = '?'
        episodes = int(ep.strip())
        try:
            genres = types[2].text.replace('Genre: ', '').strip().split(',')
        except:
            genres = '?'
        img = soup.find('div', 'anime_info_body_bg').find('img').get('src')
        if 'dub' in anime.lower():
            dub = 'DUB'
        else:
            dub = 'SUB'
        try:
            year = types[3].text.replace('Released: ', '').strip()
        except:
            year = '?'
        try:
            typo = types[0].text.replace('Type: ', '').strip()
        except:
            typo = '?'
        season = typo
        try:
            status = types[4].text.replace('Status: ', '').strip()
        except:
            status = '?'

        return (title, synopsis, names, studios, episodes, genres, img, dub, season, year, typo, status)

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
        anime_id = bs(requests.get(
            f'https://{self.host}/category/{anime}').content, 'html.parser').find('input', 'movie_id').get('value')

        html = bs(requests.get(
            f'https://ajax.gogo-load.com/ajax/load-list-episode?ep_start=0&ep_end=100000&id={anime_id}').content, 'html.parser')

        li = html.find_all('li')
        eps = []
        for i in li:
            a = i.find('a').get('href').strip()[1:]
            eps.append(a)
        eps.reverse()
        return len(li), eps

    def get_links(self, url):
        anime = url
        data = {}

        soup = bs(requests.get(
            f'https://{self.host}/{url}').content, 'html.parser')
        div = soup.find('div', 'anime_muti_link')
        a = div.find_all('a')
        embeds = []

        for i in a:
            url = i.get('data-video')
            if not url.startswith('https'):
                url = 'https:'+url

            if 'mixdrop.co' in url:
                url = url.replace('mixdrop.co', 'mixdrop.ch')

            if 'mp4upload' not in url:
                embeds.append(url)
        dlink = soup.find('li', 'dowloads').find('a').get('href')
        if 'dub' in anime:
            data['DUB'] = embeds[1:]
            data['DL'] = {}
            data['DL']['DUB'] = dlink
        else:
            data['SUB'] = embeds[1:]
            data['DL'] = {}
            data['DL']['SUB'] = dlink
            anime = anime.split(
                '-episode-')[0] + '-dub' + '-episode-' + anime.split('-episode-')[1]
            soup = bs(requests.get(
                f'https://{self.host}/{anime}').content, 'html.parser')
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

                if 'mixdrop.co' in url:
                    url = url.replace('mixdrop.co', 'mixdrop.ch')

                if 'mp4upload' not in url:
                    embeds.append(url)

            dlink = soup.find('li', 'dowloads').find('a').get('href')
            data['DUB'] = embeds[1:]
            data['DL']['DUB'] = dlink
            return data
        return data
