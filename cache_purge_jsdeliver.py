import requests

urls = ['https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/css/anime.min.css',
       'https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/css/episode.min.css',
       'https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/css/home.min.css',
       'https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/css/search.min.css',
       'https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/css/video.min.css',
       'https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/js/home.min.js',
       'https://cdn.jsdelivr.net/gh/TechShreyash/AnimeDex@main/static/js/player.min.js']


for url in urls:
    url = url[24:]
    r = requests.get('https://purge.jsdelivr.net'+url)
    print(r.json().get('status'), url)
