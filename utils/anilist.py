from datetime import datetime
import requests

cache = {"recommend": {}}


def get_season(future: bool = False):
    k = datetime.now()
    m = k.month
    if future:
        m = m + 3
    y = k.year
    if m > 12:
        y = y + 1
    if m in [1, 2, 3] or m > 12:
        return "WINTER", y
    if m in [4, 5, 6]:
        return "SPRING", y
    if m in [7, 8, 9]:
        return "SUMMER", y
    if m in [10, 11, 12]:
        return "FALL", y


class Anilist:
    def __init__(self) -> None:

        self.BROWSE_QUERY = """
query ($s: MediaSeason, $y: Int, $sort: [MediaSort]) {
    Page (perPage:10) {
        media (season: $s, seasonYear: $y, sort: $sort) {
    	    title {
                romaji
                english
                native
            }
            format
            genres
            episodes
            bannerImage
            coverImage{
                medium
            }
            type
            status
            description
        }
    }
}
"""
        self.ANIME_QUERY = """
query ($id: Int, $idMal: Int, $search: String) {
  Media(id: $id, idMal: $idMal, search: $search, type: ANIME) {
    id
    idMal
    title {
      romaji
      english
      native
    }
    format
    status
    episodes
    seasonYear
    season
    description
    studios(sort: FAVOURITES_DESC, isMain: true) {
      nodes {
        name
      }
    }
    bannerImage
    coverImage {
      medium
    }
    genres
    averageScore
    recommendations {
      edges {
        node {
          id
          mediaRecommendation {
            id
            title {
              romaji
              english
              native
            }
            status
            episodes
            coverImage {
              medium
            }
            bannerImage
            format
            meanScore
          }
        }
      }
    }
  }
}
"""
        self.RECOMMENDATIONS = """
        query ($id: Int, $idMal: Int, $search: String) {
  Media(id: $id, idMal: $idMal, search: $search, type: ANIME) {
    recommendations {
      edges {
        node {
          id
          mediaRecommendation {
            id
            title {
              romaji
              english
              native
            }
            status
            episodes
            coverImage {
              medium
            }
            bannerImage
            format
            meanScore
          }
        }
      }
    }
  }
}

        """

    def trending(self):
        if cache.get("trending"):
            return cache.get("trending")

        s, y = get_season()
        vars = {"s": s, "y": y, "sort": "TRENDING_DESC"}
        data = requests.post(
            "https://graphql.anilist.co",
            json={"query": self.BROWSE_QUERY, "variables": vars},
        ).json()
        data = data.get("data").get("Page").get("media")
        if data:
            cache["trending"] = data
        return data

    def popular(self):
        if cache.get("popular"):
            return cache.get("popular")

        s, y = get_season()
        vars = {"s": s, "y": y, "sort": "POPULARITY_DESC"}
        data = requests.post(
            "https://graphql.anilist.co",
            json={"query": self.BROWSE_QUERY, "variables": vars},
        ).json()
        data = data.get("data").get("Page").get("media")
        if data:
            cache["popular"] = data
        return data

    def anime(self, anime):
        s, y = get_season()
        vars = {"search": anime}
        data = requests.post(
            "https://graphql.anilist.co",
            json={"query": self.ANIME_QUERY, "variables": vars},
        ).json()
        return data.get("data").get("Media")

    def get_recommendation(self, anime):
        if cache.get("recommend").get(anime):
            return cache.get("recommend").get(anime)

        s, y = get_season()
        vars = {"search": anime}
        data = requests.post(
            "https://graphql.anilist.co",
            json={"query": self.ANIME_QUERY, "variables": vars},
        ).json()
        data = data.get("data").get("Media")
        if data:
            cache["recommend"][anime] = data
        return data

