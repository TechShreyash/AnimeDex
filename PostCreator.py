import os
import random
from programs.deprecated.frenzyScrapper import animeFrenzy_scrapper, newPost_scrapper
from programs.db import del_inDB, get_all, is_inBlogger, save_inBlogger
from programs.deprecated.anilist import get_anime_img
import time
import sys
import unicodedata
print('> Starting...')

data = []
HTML = """<link href="https://fonts.googleapis.com" rel="preconnect"></link>
<link crossorigin="" href="https://fonts.gstatic.com" rel="preconnect"></link>
<link href="https://fonts.googleapis.com/css2?family=Noto+Sans&amp;display=swap" rel="stylesheet"></link>
<link href="https://cdnjs.cloudflare.com/ajax/libs/font-awesome/4.7.0/css/font-awesome.min.css" rel="stylesheet"></link>

<div style="text-align: center;">
    <img src="{img}"/>
    <br />
    <h1 style="clear: both; color: #ff2400; font-family: Roboto; font-size: large; text-align: center;">{oname}</h1>
    <hr />
    <div style="font-family: &quot;Noto Sans&quot;, sans-serif; text-align: left;">
        <h2 style="clear: both; color: #ff2400; font-family: Roboto, sans-serif; font-size: medium; text-align: left;">
            Series Info :</h2>

        <ul style="list-style-type: circle;">
            <li><span>Name :&nbsp;{title}</span></li>
            <li><span>Format :&nbsp;{form}</span></li>
            <li><span>Genre : {genre}</span></li>
            <li><span>Episodes : {eps}</span></li>
            <li><span>Duration :&nbsp;24 min</span></li>
            <li><span>Status :&nbsp;{status}</span></li>
            <li><span>Language : {lang}</span></li>
        </ul>
    </div>

    <hr />

    <h2 style="clear: both; color: #ff2400; font-family: &quot;Noto Sans&quot;, sans-serif; font-size: medium; text-align: left;">
        Synopsis :</h2>
    <div style="text-align: left;">{synopsis}</div>
    <hr />

    <h2 style="clear: both; color: #ff2400; font-family: &quot;Noto Sans&quot;, sans-serif; font-size: medium; text-align: left;">
        Download Links :</h2>
    <a href="{download}" target="_blank"><button class="btn" style="width: auto;"><i class="fa fa-download"></i> Download</button></a>
</div>
"""


def getName(url):
    if url[-1] == '/':
        url = url[:-1]
    name = url.split('/')[-1]
    name = name.split('-episode-')[0]
    return name


def get_post():
    global data
    post = None
    print('> Choosing Post')

    while post == None:
        temp = random.choice(data)
        title = temp[3]
        if is_inBlogger(title):
            print('> Already Uploaded - Skipping :', title)
            data.remove(temp)
            try:
                del_inDB(temp)
            except:
                pass
        else:
            print('> Selected :', title)
            post = temp
    return post


def generate_html(post):
    print('> Getting Details...')
    name = getName(post[7])
    adata = animeFrenzy_scrapper(name)

    title = adata[0]
    labels = [adata[1]]
    details = adata[2]
    eps = adata[3][2]
    oname = adata[3][0].replace(',', ' |')
    oname = unicodedata.normalize('NFKD', oname).encode(
        'ascii', 'ignore').decode('ascii', 'ignore').strip()

    if oname != '':
        while oname[-1] == ' ' or oname[-1] == '|':
            oname = oname[:-1]
    else:
        oname = ''

    labels.append(adata[3][1])
    labels.append(adata[4])

    for i in adata[5]:
        labels.append(i)

    ltext = ''
    for i in labels:
        ltext += i + ', '
    ltext = ltext[:-2]

    img = get_anime_img(title)
    if img == 'eror':
        img = post[2]

    output = HTML.format(
        title=title,
        labels=ltext,
        form=labels[0],
        genre=ltext,
        eps=eps,
        status=labels[2],
        lang=labels[1],
        synopsis=details,
        download=f'/anime/{name}',
        oname=oname,
        img=img
    )

    output = unicodedata.normalize('NFKD', output).encode(
        'ascii', 'ignore').decode('ascii', 'ignore').strip()

    with open('website.html', 'w') as f:
        f.write(output)
    return title, ltext


def upload(title, ltext):
    print(f'> Uploading {title} To Website')
    os.system(
        f'easyblogger --blogid 5684752010091795745 post -t "{title}" -l "{ltext}" --publish -f website.html')

    print('> Saving Anime Data In Database')
    save_inBlogger(title)


def postCreator():
    print('> Fetching Posts From Database...')
    global data
    data = get_all()
    x = []

    for i in data:
        x.append(i['name'])
    data = x

    totalp = len(data)
    print(f'> Total {totalp} posts...')

    num = 0 #int(input('> How many post do you want to upload ? :- '))

    if num == 0:
        num = totalp
        print('> Uploading All Posts...')

    for i in range(1,num+1):
        err = 0
        try:
            print('-'*40)
            print(f'{i}/{num}')

            post = get_post()
            title, label = generate_html(post)
            upload(title,label)
            data.remove(post)
        except:
            err += 1
        if err == 0:
            del_inDB(post)
    print('-'*40)
    print('\n> Done... Closing in 10 seconds')
    time.sleep(10)
    sys.exit()

if __name__ == '__main__':
    postCreator()