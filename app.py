
import time
from programs.cache import HOME
from programs.gogoScrapper import GoGoApi
GOGO = GoGoApi()
from programs.others import get_atitle, get_other_title, get_studios, get_t_from_u
from programs.anilist import Anilist

from flask import Flask, render_template, request, redirect
from programs.html_gen import animeRecHtml, episodeHtml, get_eps_html, get_recent_html, get_selector_btns, get_genre_html, get_trending_html, slider_gen
import random
app = Flask(__name__)


@app.route('/')
def hello_world():
    t1 = time.time()
    t2 = HOME.get('time')
    cache = HOME.get('cache')
    if t2 and cache:
        if ((t1-t2)/60) < 10:
            return cache

    html = render_template('home.html')
    div1 = get_trending_html()
    div2 = get_recent_html(GOGO.home())

    sliders = slider_gen()

    html = html.replace(
        'MOST_POPULAR',
        div1
    ).replace(
        'RECENT_RELEASE',
        div2
    ).replace(
        'SLIDERS',
        sliders
    )
    HOME['time'] = t1
    HOME['cache'] = html
    return html


@app.route('/embed')
def get_embed():
    url = request.args.get('url')
    if url and '.m3u8' not in url:
        return redirect(url)

    if '.m3u8' in url:
        file = url
    else:
        file = request.args.get('file')
    sub = request.args.get('sub')
    title = request.args.get('title')
    if sub != None:
        track = """tracks: [{
                "kind": "captions",
                file: "sopu",
                label: 'English',
                "default": true
            }],""".replace('sopu', sub)
    else:
        track = ''

    return render_template('vid.html', m3u8=file, title=title).replace('TRACKS', track)




@app.route('/episode/<anime>/<episode>')
def get_episode(anime, episode):
    search = GOGO.search(anime, True)
    eps = GOGO.get_links(search[0], episode)
    # sl, cur = get_selector_btns(
    #      f"/episode/{anime}/", episode, len(eps))
    ep_html, iframe = episodeHtml(eps, f'{anime} - Episode {episode}')

    temp = render_template(
        'episode.html',
        title=f'{anime} - Episode {episode}',
        heading=anime,
        iframe=iframe
    )
    sl = ''

    return temp.replace('PROSLO', sl).replace('SERVER', ep_html)


@app.route('/anime/<anime>')
def get_anime(anime):
    if '.' in anime:
        anime = anime.split('.')[0].replace('-', ' ')
    data = Anilist.anime(get_t_from_u(anime))

    title = get_atitle(data.get('title'))
    synopsis = data.get('description')
    names = get_other_title(data.get('title'))
    studios = get_studios(data.get('studios'))
    episodes = 'Ep ' + str(data.get('totalEpisodes'))
    genres = get_genre_html(data.get('genres'))
    displayAnime = animeRecHtml(data.get('recommendations'))
    ep_html = get_eps_html(anime, title)

    html = render_template('anime.html',
                           img=data.get('image'),
                           title=title,
                           DUB=data.get('type'),
                           SEASON=data.get('season'),
                           other=names,
                           studios=studios,
                           episodes=episodes,
                           year=data.get('releaseDate'),
                           ATYPE=data.get('type'),
                           status=data.get('status'),
                           animeURL=f'/anime/{anime}',
                           WATCHNOW=f'/episode/{anime}',
                           aid=anime
                           )

    html = html.replace('GENEROS', genres)
    html = html.replace('EPISOS', ep_html)
    html = html.replace('DISPLAY_ANIME', displayAnime)
    html = html.replace('SYNOP', synopsis)
    return html


@app.route('/search', methods=['GET'])
def search_anime():
    anime = request.args.get('query')

    html = render_template('search.html',
                           aid=anime.replace('+', ' '))
    data = searchScrapper(anime)
    display = anime_display_html(data)

    html = html.replace(
        'SEARCHED',
        display
    )
    return html


if __name__ == '__main__':
    app.run('0.0.0.0')
