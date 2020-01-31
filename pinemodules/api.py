import requests
import json
import urllib
from . import __version__

URL = 'http://172.16.42.1:1471/api/'

class API(object):
    def __init__(self, apiToken, url = None):
        super(API, self).__init__();
        self.apiToken = apiToken
        self.url = url if url else URL
        self.userAgent = 'WallofSheep' + __version__
        self.headers = {'User-Agent': self.userAgent, 'Content-Type': 'application/json', 'Accept': 'application/json,'}
    def request(self, type, module, action, args = None):
        requestObject = {'apiToken': self.apiToken, type: module, 'action': action}
        if args:
            requestObject.update(args)
        payload = json.dumps(requestObject)
        resp = requests.post(self.url, data=payload, headers=self.headers)
        try:
            return json.loads(resp.text.replace(")]}',\n",''))
        except ValueError as e:
            print(e)
