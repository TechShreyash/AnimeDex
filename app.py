from utils.db import update_views, update_watch
from utils.html_gen import (
    animeRecHtml,
    animeRecHtml2,
    episodeHtml,
    get_eps_html,
    get_eps_html2,
    get_recent_html,
    get_search_html,
    get_selector_btns,
    get_genre_html,
    get_trending_html,
    slider_gen,
)
from flask import Flask, render_template, request, redirect, send_file
from utils.anilist import Anilist
from utils.others import get_atitle, get_other_title, get_studios, get_t_from_u
from utils.techzapi import TechZApi
from config import API_KEY

app = Flask(__name__)
TechZApi = TechZApi(API_KEY)


@app.route("/favicon.ico")
def favicon():
    return redirect(
        "https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/img/favicon.ico"
    )


@app.route("/")
def home():
    html = render_template("home_min.html")
    div1 = get_trending_html(TechZApi.top_animedex())
    div2 = get_recent_html(TechZApi.gogo_latest())
    sliders = slider_gen()

    html = (
        html.replace("MOST_POPULAR", div1)
        .replace("RECENT_RELEASE", div2)
        .replace("SLIDERS", sliders)
    )
    update_views("home-animedex")
    return html


@app.route("/anime/<anime>")
def get_anime(anime):
    try:
        data = TechZApi.gogo_anime(anime)
        TITLE = data.get("title")
        IMG = data.get("img")
        LANG = data.get("lang")
        TYPE = data.get("type")
        WATCHNOW = "/episode/" + data.get("id") + "/1"
        OTHER = data.get("other name")
        TOTAL = str(data.get("total_ep"))
        YEAR = data.get("year")
        STATUS = data.get("status")
        STUDIO = "?"
        GENERES = get_genre_html(data.get("genre").split(","))
        SYNOPSIS = data.get("summary")

        x = anime.lower()
        if x.endswith("-dub"):
            x = x[:-4]
        if x.endswith("-sub"):
            x = x[:-4]
        x = get_t_from_u(x).replace("-", " ")

        try:
            DISPLAY_ANIME = animeRecHtml(Anilist().get_recommendation(x))
        except:
            DISPLAY_ANIME = ""
        EPISODES = get_eps_html(data=data.get("episodes"))

        html = render_template(
            "anime_min.html",
            IMG=IMG,
            TITLE=TITLE,
            LANG=LANG,
            TYPE=TYPE,
            WATCHNOW=WATCHNOW,
            OTHER=OTHER,
            TOTAL=TOTAL,
            YEAR=YEAR,
            STATUS=STATUS,
            STUDIO=STUDIO,
        )
    except:
        anime = anime.lower()
        if anime.endswith("-dub"):
            anime = anime[:-4]
        if anime.endswith("-sub"):
            anime = anime[:-4]
        anime = get_t_from_u(anime).replace("-", " ")
        data = Anilist().anime(anime)

        IMG = data.get("coverImage").get("medium").replace("small", "medium")
        if not IMG:
            IMG = data.get("bannerImage")
        TITLE = get_atitle(data.get("title"))
        SYNOPSIS = data.get("description")
        OTHER = get_other_title(data.get("title"))
        STUDIO = get_studios(data.get("studios").get("nodes"))
        TOTAL = str(data.get("episodes"))
        GENERES = get_genre_html(data.get("genres"))
        DISPLAY_ANIME = animeRecHtml2(data.get("recommendations").get("edges"))

        try:
            EPISODES, id = get_eps_html(api=TechZApi, anime=TITLE)
        except:
            EPISODES, id = "", "#"

        SEASON = str(data.get("season")) + " " + str(data.get("seasonYear"))
        YEAR = data.get("seasonYear")
        TYPE = data.get("format")
        STATUS = data.get("status")
        WATCHNOW = "/episode/" + id + "/1"

        html = render_template(
            "anime_min.html",
            IMG=IMG,
            TITLE=TITLE,
            LANG=TYPE,
            TYPE=SEASON,
            WATCHNOW=WATCHNOW,
            OTHER=OTHER,
            TOTAL=TOTAL,
            YEAR=YEAR,
            STATUS=STATUS,
            STUDIO=STUDIO,
        )

    html = html.replace("GENERES", GENERES)
    html = html.replace("EPISODES", EPISODES)
    html = html.replace("DISPLAY_ANIME", DISPLAY_ANIME)
    html = html.replace("SYNOPSIS", SYNOPSIS)
    update_views(anime)
    return html


@app.route("/episode/<anime>/<episode>")
def get_episode(anime, episode):
    anime = get_t_from_u(anime).lower()
    episode = int(episode)

    try:
        data = TechZApi.gogo_episode(f"{anime}-episode-{episode}")
        x = TechZApi.gogo_anime(anime)
        total_eps = x.get("total_ep")
        ep_list = x.get("episodes")
    except:
        search = TechZApi.gogo_search(anime)[0]
        anime = search.get("id")
        total_eps = search.get("total_ep")
        ep_list = search.get("episodes")
        data = TechZApi.gogo_episode(f"{anime}-episode-{episode}")

    if str(request.args.get("download", True)).lower() == "false":
        dl = False
    else:
        dl = True

    if str(request.args.get("selector", True)).lower() == "false":
        btn_html = ""
    else:
        btn_html = get_selector_btns(f"/episode/{anime}/", int(episode), int(total_eps))

    ep_html, iframe = episodeHtml(data, f"{anime} - Episode {episode}", dl=dl)

    if str(request.args.get("embed", False)).lower() == "true":
        temp = render_template(
            "embed_min.html",
            title=f"{anime} - Episode {episode}",
            heading=anime,
            iframe=iframe,
        )

        if str(request.args.get("eplist", False)).lower() == "true":
            ep_list = get_eps_html2(ep_list)
            temp = temp.replace(
                "LISTHTML",
                "<div class=divo><h2>List Of Episodes:</h2><div class=divo2>EPISOS</div></div>",
            ).replace("EPISOS", ep_list)
        else:
            temp = temp.replace("LISTHTML", "")

    else:
        ep_list = get_eps_html2(ep_list)
        temp = render_template(
            "episode_min.html",
            title=f"{anime} - Episode {episode}",
            heading=anime,
            iframe=iframe,
        ).replace("EPISOS", ep_list)

    update_watch(anime)
    return temp.replace("PROSLO", btn_html).replace("SERVER", ep_html)


@app.route("/search", methods=["GET"])
def search_anime():
    anime = request.args.get("query").lower().strip()

    if anime.endswith("-dub"):
        anime = anime[:-4]
    if anime.endswith("-sub"):
        anime = anime[:-4]

    html = render_template("search_min.html", aid=anime.replace("+", " "))

    data = TechZApi.gogo_search(anime)
    display = get_search_html(data)

    html = html.replace("SEARCHED", display)
    update_views("search-animedex")
    return html


@app.route("/embed")
def get_embed():
    try:
        url = request.args.get("url")
        file = False
        if url:
            if ".mp4" in url or ".mkv" in url:
                file = url
            else:
                if request.args.get("token"):
                    url += f'&token={request.args.get("token")}'
                if request.args.get("expires"):
                    url += f'&expires={request.args.get("expires")}'

                file = TechZApi.gogo_stream(url)
                server = int(request.args.get("server"))
                if server == 1:
                    file = file.get("source")[0].get("file")
                elif server == 2:
                    file = file.get("source_bk")[0].get("file")
        else:
            file = request.args.get("file")
    except:
        file = request.args.get("file")
    if not file:
        return redirect(url)
    title = request.args.get("title")

    return render_template("vid_min.html", m3u8=file, title=title)


@app.route("/api/latest/<page>")
def latest(page):
    try:
        data = TechZApi.gogo_latest(page)
        html = get_recent_html(data)
        return {"html": html}
    except:
        return {"html": ""}


@app.route("/robots.txt")
def robots_txt():
    try:
        return send_file("static/robots.txt")
    except:
        return {"html": ""}
