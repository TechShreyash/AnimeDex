from programs.anime_loader import get_GPage, get_html
from programs.db import update_views, update_watch
from programs.html_gen import animeRecHtml, episodeHtml, get_eps_html, get_eps_html2, get_recent_html, get_search_html, get_selector_btns, get_genre_html, get_trending_html, slider_gen
from flask import Flask, render_template, request, redirect
from programs.anilist import Anilist
from programs.others import get_atitle, get_other_title, get_studios, get_t_from_u
from programs.gogo import GoGoApi
from programs.vidstream import extract_m3u8

GOGO = GoGoApi()
app = Flask(__name__)


@app.route('/favicon.ico')
def favicon():
    return redirect('https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/img/favicon.ico')


@app.route('/')
def home():
    html = render_template('home.min.html')
    div1 = get_trending_html()
    try:
        div2 = get_recent_html(GOGO.home())
    except:
        div2 = ''
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
    update_views('home-animedex')
    return html


@app.route('/anime/<anime>')
def get_anime(anime):
    try:
        data = GOGO.anime(anime)
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
        x = anime.lower()
        if x.endswith('-dub'):
            x = x[:-4]
        if x.endswith('-sub'):
            x = x[:-4]
        x = get_t_from_u(x).replace('-', ' ')
        displayAnime = animeRecHtml(Anilist().get_recommendation(x))
        ep_html, watch = get_eps_html(anime, anime)
    except:
        anime = anime.lower()
        if anime.endswith('-dub'):
            anime = anime[:-4]
        if anime.endswith('-sub'):
            anime = anime[:-4]
        anime = get_t_from_u(anime).replace('-', ' ')
        data = Anilist().anime(anime)

        img = data.get('coverImage').get('medium').replace('small', 'medium')
        if not img:
            img = data.get('bannerImage')
        title = get_atitle(data.get('title'))
        synopsis = data.get('description')
        names = get_other_title(data.get('title'))
        studios = get_studios(data.get('studios').get('nodes'))
        episodes = str(data.get('episodes'))
        genres = get_genre_html(data.get('genres'))
        displayAnime = animeRecHtml(data.get('recommendations').get('edges'))
        try:
            ep_html, watch = get_eps_html(anime)
        except:
            ep_html, watch = '', '#'
        dub = data.get('format')
        season = data.get('season')
        year = data.get('seasonYear')
        typo = data.get('format')
        status = data.get('status')

    html = render_template('anime.min.html',
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
                           animeURL=f'/anime/{anime}',
                           WATCHNOW=f'/episode/{watch}',
                           aid=anime
                           )

    html = html.replace('GENEROS', genres)
    html = html.replace('EPISOS', ep_html)
    html = html.replace('DISPLAY_ANIME', displayAnime)
    html = html.replace('SYNOP', synopsis)
    update_views(anime)
    return html


@app.route('/episode/<anime>/<episode>')
def get_episode(anime, episode):
    anime = get_t_from_u(anime).lower()
    episode = int(episode)

    try:
        total_eps, ep = GOGO.get_episodes(anime)
        eps = GOGO.get_links(ep[episode-1])
        ep_list = get_eps_html2(ep)
    except:
        search = GOGO.search(anime, True)
        total_eps, ep = GOGO.get_episodes(search[0])
        eps = GOGO.get_links(ep[episode-1])
        ep_list = get_eps_html2(ep)

    aid = ep[episode-1].split('-episode-')[0]

    btn_html = get_selector_btns(
        f"/episode/{anime}/", int(episode), int(total_eps))
    ep_html, iframe = episodeHtml(eps, f'{anime} - Episode {episode}')

    temp = render_template(
        'episode.min.html',
        title=f'{anime} - Episode {episode}',
        heading=anime,
        iframe=iframe
    )

    update_watch(aid)
    return temp.replace('PROSLO', btn_html).replace('SERVER', ep_html).replace('EPISOS', ep_list)


@app.route('/search', methods=['GET'])
def search_anime():
    anime = request.args.get('query').lower().strip()

    if anime.endswith('-dub'):
        anime = anime[:-4]
    if anime.endswith('-sub'):
        anime = anime[:-4]

    html = render_template('search.min.html',
                           aid=anime.replace('+', ' '))

    data = GOGO.search(anime)
    display = get_search_html(data)

    html = html.replace(
        'SEARCHED',
        display
    )
    update_views('search-animedex')
    return html


@app.route('/embed')
def get_embed():
    url = request.args.get('url')
    if url:
        if 'gogohd' in url:
            if request.args.get('token'):
                url += f'&token={request.args.get("token")}'
            if request.args.get('expires'):
                url += f'&expires={request.args.get("expires")}'
            file = extract_m3u8(url)
        elif '.mp4' in url or '.mkv' in url:
            file = url
        else:
            file = request.args.get('file')
    if not file:
        return redirect(url)
    sub = request.args.get('sub')
    title = request.args.get('title')
    if sub != None:
        track = """tracks: [{"kind": "captions", file: "sopu", label: 'English', "default": true}],""".replace(
            'sopu', sub)
    else:
        track = ''

    return render_template('vid.min.html', m3u8=file, title=title).replace('TRACKS', track)


@app.route('/api/latest/<page>')
def latest(page):
    try:
        data = get_GPage(page)
        html = get_html(data)
        return {'html': html}
    except:
        return {'html': ''}


if __name__ == '__main__':
    app.run('0.0.0.0', debug=True)
