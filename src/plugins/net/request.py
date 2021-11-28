import requests
from requests.exceptions import ConnectionError

'''
    Plugin qui envoie un request via Call
    Un remplacement est possible dans l'uri en utilisant data1 et data2
    Ex : 
    -   F"/api/scenes/{}/subscenes/{}"
    -   /api/scenes/ev.data1/subscenes/ev.data2
'''

class RequestBase():
    def __init__(self, uri):
        self.uri = uri

    def get(self, ev):
        try:
            r = requests.get(self.uri.format(ev.data1, ev.data2))
            if r.status_code not in [200, 204]:
                print(r.status_code) 
        except Exception:
            print(500)

    def post(self):
        print(501)

    def delete(self):
        print(501)

    def put(self):
        print(501)

''' GET '''
class RequestGet(RequestBase):
    def __init__(self, uri):
        super().__init__(uri)

    def __call__(self, ev):
        super().get(ev)

class RequestPost(RequestBase):
    def __init__(self, uri):
        super().__init__(uri)

    def __call__(self, ev):
        super().post()

class RequestDelete(RequestBase):
    def __init__(self, uri):
        super().__init__(uri)

    def __call__(self, ev):
        super().delete()

