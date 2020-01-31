from .api import API

class Module(object):
    def __init__(self, api, name, system = False):
        super(Module, self).__init__()
        self.api = api
        self.name = name
        self.type = 'system' if system else 'module'
    def request(self, action, args = None):
        return self.api.request(self.type, self.name, action, args)