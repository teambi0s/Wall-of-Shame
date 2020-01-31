from .api import API
from . import modules
import  requests

class Pineapple(object):
    def __init__(self, apiKey, apiUrl = None, debug = False):
        super(Pineapple, self).__init__()
        self.debug = debug
        self.api = API(apiKey, apiUrl)
        self.modules = {}
        self._pineappleModule = __import__('pinemodules')
        for moduleName in modules:
            moduleClass = self._pineappleModule.__dict__[moduleName].__dict__[moduleName.title()]
            self.modules[moduleName] = moduleClass(self.api)

    def getModule(self, module):
        return self.modules[module]
