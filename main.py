from programs.html_gen import animeRecHtml, episodeHtml, get_eps_html, get_recent_html, get_search_html, get_selector_btns, get_genre_html, get_trending_html, slider_gen
from flask import Flask, render_template, request, redirect
from programs.anilist import Anilist
from programs.others import get_atitle, get_other_title, get_studios, get_t_from_u
from programs.gogo import GoGoApi
GOGO = GoGoApi()
app = Flask(__name__)


@app.route('/')
def hello_world():
    html = render_template('home.html')
    div1 = get_trending_html()
    div2 = get_recent_html(GOGO.home())
    sliders, slider = slider_gen()

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
    if url and '.m3u8' not in url:
        return redirect(url)

    if '.m3u8' in url or '.mp4' in url or '.mkv' in url:
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
    anime = anime.lower().replace('sub','').replace('dub','')
    anime = get_t_from_u(anime)
    search = GOGO.search(anime, True)

    total_eps = GoGoApi().get_episodes(search[0])

    eps = GOGO.get_links(search[0], episode)
    btn_html = get_selector_btns(f"/episode/{anime}/", int(episode), int(total_eps))
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
    anime = anime.lower().replace('sub','').replace('dub','')
    if '.' in anime:
        anime = anime.split('.')[0].replace('-', ' ')
    
    try:
        data = Anilist.anime(get_t_from_u(anime))
        title = get_atitle(data.get('title'))
        synopsis = data.get('description')
        names = get_other_title(data.get('title'))
        studios = get_studios(data.get('studios'))
        episodes = str(data.get('totalEpisodes'))
        genres = get_genre_html(data.get('genres'))
        displayAnime = animeRecHtml(data.get('recommendations'))
        ep_html = get_eps_html(anime, title)
    except:
        data = GOGO.anime(get_t_from_u(anime))


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
                           WATCHNOW=f'/episode/{anime}/1',
                           aid=anime
                           )

    html = html.replace('GENEROS', genres)
    html = html.replace('EPISOS', ep_html)
    html = html.replace('DISPLAY_ANIME', displayAnime)
    html = html.replace('SYNOP', synopsis)
    return html


@app.route('/search', methods=['GET'])
def search_anime():
    anime = request.args.get('query').lower().replace('sub','').replace('dub','')

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