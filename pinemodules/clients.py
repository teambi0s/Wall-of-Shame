from .module import Module

class Clients(Module):
    def __init__(self, api):
        super(Clients, self).__init__(api, 'Clients')
    def getClientData(self):
        return self.request('getClientData')
