import requests
from requests.exceptions import ConnectionError

'''
    Plugin qui envoie un Http via Call
    Un remplacement est possible dans l'uri en utilisant data1 et data2
    Ex : 
    -   F"/api/scenes/{}/subscenes/{}"
    -   /api/scenes/ev.data1/subscenes/ev.data2
'''

''' Abstract '''
class HttpClientBase():
    def __init__(self, config, uri):
        self.enable = config["enable"]
        self.uri = uri

    def get(self, ev):
        if not self.enable:
            return

        try:
            r = requests.get(self.uri.format(ev.data1, ev.data2))
            if r.status_code not in [200, 300]:
                print(r.status_code) 
        except Exception:
            print(500)

    def post(self, ev):
        if not self.enable:
            print(501)

    def delete(self, ev):
        if not self.enable:
            print(501)

    def put(self, ev):
        if not self.enable:
            print(501)


''' 
    Childs 
'''
class HttpGet(HttpClientBase):
    def __init__(self, config, uri):
        super().__init__(config, uri)

    def __call__(self, ev):
        super().get(ev)

class HttpPost(HttpClientBase):
    def __init__(self, config, uri):
        super().__init__(config, uri)

    def __call__(self, ev):
        super().post(ev)

class HttpPut(HttpClientBase):
    def __init__(self, config, uri):
        super().__init__(config, uri)

    def __call__(self, ev):
        super().put(ev)

class HttpDelete(HttpClientBase):
    def __init__(self, config, uri):
        super().__init__(config, uri)

    def __call__(self, ev):
        super().delete(ev)

