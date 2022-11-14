from programs.db import update_views, update_watch
from programs.html_gen import animeRecHtml, episodeHtml, get_eps_html, get_recent_html, get_search_html, get_selector_btns, get_genre_html, get_trending_html, slider_gen
from flask import Flask, render_template, request, redirect
from programs.anilist import Anilist
from programs.others import get_atitle, get_other_title, get_studios, get_t_from_u
from programs.gogo import GoGoApi
GOGO = GoGoApi()
app = Flask(__name__)


@app.route('/')
def home():
    update_views('home-animedex')
    html = render_template('home.html')
    try:
        div1 = get_trending_html()
    except:
        div1 = ''
    try:
        div2 = get_recent_html(GOGO.home())
    except:
        div2 = ''
    try:
        sliders = slider_gen()
    except:
        sliders = ''

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
    return html


@app.route('/embed')
def get_embed():
    url = request.args.get('url')
    if url:
        if '.m3u8' in url or '.mp4' in url or '.mkv' in url:
            file = url
        else:
            file = request.args.get('file')
    if not file:
        return redirect(url)
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
    anime = anime.lower()
    if anime.endswith('dub'):
        anime = anime[:-4]
    if anime.endswith('sub'):
        anime = anime[:-4]

    anime = get_t_from_u(anime)
    search = GOGO.search(anime, True)

    total_eps = GoGoApi().get_episodes(search[0])
    update_watch(search[0].strip())

    eps = GOGO.get_links(search[0], episode)
    btn_html = get_selector_btns(
        f"/episode/{anime}/", int(episode), int(total_eps))
    ep_html, iframe = episodeHtml(eps, f'{anime} - Episode {episode}')

    temp = render_template(
        'episode.html',
        title=f'{anime} - Episode {episode}',
        heading=anime,
        iframe=iframe
    )

    return temp.replace('PROSLO', btn_html).replace('SERVER', ep_html)


@app.route('/anime/<anime>')
def get_anime(anime):
    x = anime
    anime = anime.lower()
    if anime.endswith('dub'):
        anime = anime[:-4]
    if anime.endswith('sub'):
        anime = anime[:-4]

    try:
        data = Anilist.anime(get_t_from_u(anime))
        img = data.get('image')
        title = get_atitle(data.get('title'))
        synopsis = data.get('description')
        names = get_other_title(data.get('title'))
        studios = get_studios(data.get('studios'))
        episodes = str(data.get('totalEpisodes'))
        genres = get_genre_html(data.get('genres'))
        displayAnime = animeRecHtml(data.get('recommendations'))
        ep_html = get_eps_html(anime, title)
        dub = data.get('type')
        season = data.get('season')
        year = data.get('releaseDate')
        typo = data.get('type')
        status = data.get('status')
    except:
        try:
            data = GOGO.anime(x)
            title = data[0]
            synopsis = data[1]
            names = data[2]
            studios = data[3]
            episodes = data[4]
            genres = get_genre_html(data[5])
            img = data[6]
            dub = data[7]
            season = data[8]
            year = data[9]
            typo = data[10]
            status = data[11]
            displayAnime = 'Not Available'
            ep_html = get_eps_html(anime, title, episodes)
        except:
            data = GOGO.anime_api(x)
            img = data.get('image')
            title = data.get('title')
            synopsis = data.get('description')
            names = data.get('otherName')
            studios = '?'
            episodes = str(len(data.get('episodes')))
            genres = get_genre_html(data.get('genres'))
            displayAnime = 'Not Available'
            ep_html = get_eps_html(anime, title)
            dub = data.get('subOrDub').upper()
            season = data.get('type')
            year = data.get('type')
            typo = data.get('type')
            status = data.get('status')

    html = render_template('anime.html',
                           img=img,
                           title=title,
                           DUB=dub,
                           SEASON=season,
                           other=names,
                           studios=studios,
                           episodes=episodes,
                           year=year,
                           ATYPE=typo,
                           status=status,
                           animeURL=f'/anime/{x}',
                           WATCHNOW=f'/episode/{x}/1',
                           aid=anime
                           )

    html = html.replace('GENEROS', genres)
    html = html.replace('EPISOS', ep_html)
    html = html.replace('DISPLAY_ANIME', displayAnime)
    html = html.replace('SYNOP', synopsis)
    return html


@app.route('/search', methods=['GET'])
def search_anime():
    anime = request.args.get('query').lower().strip()

    if anime.endswith('dub'):
        anime = anime[:-4]
    if anime.endswith('sub'):
        anime = anime[:-4]

    html = render_template('search.html',
                           aid=anime.replace('+', ' '))

    data = GOGO.search(anime)
    display = get_search_html(data)

    html = html.replace(
        'SEARCHED',
        display
    )
    return html


if __name__ == '__main__':
    app.run('0.0.0.0')
