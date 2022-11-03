import requests

hosts = ['https://api-techshreyash.up.railway.app/',
         'https://api.consumet.org/']


class Anilist:
    def trending():
        for host in hosts:
            try:
                data = requests.get(host + 'meta/anilist/trending')
            except:
                continue
            if data.status_code == 200:
                data = data.json()
                results = data.get('results')
                if results:
                    break
        return results

    def popular():
        for host in hosts:
            try:
                data = requests.get(host + 'meta/anilist/popular')
            except:
                continue
            if data.status_code == 200:
                data = data.json()
                results = data.get('results')
                if results:
                    break
        return results

    def anime(anime):
        for host in hosts:
            data = requests.get(host + 'meta/anilist/' + anime)
            if data.status_code == 200:
                data = data.json()
                results = data.get('results')
                if results:
                    break
        if not results:
            return

        id = results[0]['id']

        for host in hosts:
            try:
                data = requests.get(host + 'meta/anilist/info/' + str(id))
            except:
                continue
            if data.status_code == 200:
                data = data.json()
                id = data.get('id')
                if id:
                    break
        return data

    def search(query):
        for host in hosts:
            data = requests.get(host + 'meta/anilist/' + query)
            if data.status_code == 200:
                data = data.json()
                results = data.get('results')
                if results:
                    break
        return results
