import requests


class PrograPedia:

    def __init__(self):
        self.url = 'https://es.wikipedia.org/w/api.php?'
        self.params = {
            'action': 'query',
            'format': 'json',
            'prop': 'info'
        }

    def receive(self, title):
        xparams = {
            'action': 'query',
            'titles': title,
            'prop': 'extracts',
            'format': 'json',
        }
        response = requests.get(self.url, params=xparams)
        r = response.json()
        #print(r)
        idx = list(r['query']['pages'].keys())[0]
        print((r['query']['pages'][str(idx)]['extract']))


class PrograPagina:
    def __init__(self, titulo, contenido, url):
        self.titulo = titulo
        self.contenido = contenido
        self.url = url
        self.id = next(PrograPagina.pid)

    def get_id():
        pid = 0
        while True:
            yield pid
            pid += 1

    pid = get_id()


if __name__ == '__main__':
    pp = PrograPedia()
    print('PrograPedia')
    while True:
        params = {
            'nose': 23
        }
        print('Ingrese termino:')
        info = input()
        pp.receive(info)

