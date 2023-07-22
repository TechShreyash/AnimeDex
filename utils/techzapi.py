import requests
import time

LATEST_CACHE = {}
SEARCH_CACHE = {"query": {}}
ANIME_CACHE = {}


class Gogo:
    def __init__(self, API_KEY) -> None:
        self.base = "https://api.techzbots.live"
        self.api_key = API_KEY

    def gogo_latest(self, page=1):
        global LATEST_CACHE

        if page in LATEST_CACHE:
            if time.time() - LATEST_CACHE.get(page, {}).get("time", 0) < 60 * 5:
                print("from cache")
                return LATEST_CACHE[page]["results"]

        data = requests.get(
            f"{self.base}/gogo/latest?api_key={self.api_key}&page={page}"
        ).json()

        if len(data["results"]) != 0:
            LATEST_CACHE[page] = {"time": time.time(), "results": data["results"]}
        return data["results"]

    def gogo_anime(self, anime):
        global ANIME_CACHE

        if anime in ANIME_CACHE:
            if time.time() - ANIME_CACHE.get(anime, {}).get("time", 0) < 60 * 60:
                print("from cache")
                return ANIME_CACHE[anime]["results"]

        data = requests.get(
            f"{self.base}/gogo/anime?id={anime}&api_key={self.api_key}"
        ).json()

        if len(data) != 0:
            ANIME_CACHE[anime] = {"time": time.time(), "results": data["results"]}
        return data["results"]

    def gogo_search(self, query):
        global SEARCH_CACHE

        if query in SEARCH_CACHE.get("query", {}):
            print("from cache")
            return SEARCH_CACHE["query"][query]

        if time.time() - SEARCH_CACHE.get("time", 0) < 60 * 60:
            SEARCH_CACHE = {"time": time.time(), "query": {}}

        data = requests.get(
            f"{self.base}/gogo/search/?query={query}&api_key={self.api_key}"
        ).json()

        if len(data["results"]) != 0:
            SEARCH_CACHE["query"][query] = data["results"]
        return data["results"]

    def gogo_episode(self, episode):
        data = requests.get(
            f"{self.base}/gogo/episode?id={episode}&api_key={self.api_key}&lang=both"
        ).json()["results"]

        if data.get("SUB"):
            data["SUB"] = [
                data["SUB"][0] + "&server=1",
                data["SUB"][0] + "&server=2",
                data["SUB"][1] + "&server=1",
                data["SUB"][1] + "&server=2",
            ] + data["SUB"][2:]
        if data.get("DUB"):
            data["DUB"] = [
                data["DUB"][0] + "&server=1",
                data["DUB"][0] + "&server=2",
                data["DUB"][1] + "&server=1",
                data["DUB"][1] + "&server=2",
            ] + data["DUB"][2:]

        return data

    def gogo_stream(self, url):
        url = str(requests.utils.quote(url))
        data = requests.get(
            f"{self.base}/gogo/stream?url={url}&api_key={self.api_key}"
        ).json()
        return data["results"]


TOP_CACHE = {}


class TechZApi(Gogo):
    def __init__(self, API_KEY) -> None:
        self.base = "https://api.techzbots.live"
        self.api_key = API_KEY
        super().__init__(API_KEY)

    def top_animedex(self):
        global TOP_CACHE

        if time.time() - TOP_CACHE.get("time", 0) < 60 * 60 * 24:
            print("from cache")
            return TOP_CACHE["results"]
        try:
            data = (
                requests.get("https://api.animedex.live/top").json().get("top")
            )
            TOP_CACHE = {"time": time.time(), "results": data}
            return data
        except:
            pass
