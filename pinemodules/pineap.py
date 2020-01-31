import json
from .module import Module

class Pineap(Module):
    def __init__(self, api):
        super(Pineap, self).__init__(api, 'PineAP')
    def getSSIDPool(self):
        return self.request('getPool')
    def clearPool(self):
        return self.request('clearPool')
    def addSSID(self, ssid):
        ssidname = ssid
        print('Adding '+ssidname)
        return self.request('addSSID', {'ssid': ssid})
    def removeSSID(self, ssid):
        return self.request('removeSSID', {'ssid': ssid})
    def setPineAPSettings(self, settings):
        self.request('setPineAPSettings', {'settings': json.dumps(settings)})
    def getPineAPSettings(self):
        return self.request('getPineAPSettings')
    def deauth(self, sta, clients, multiplier, channel):
        multiplier = 10 if multiplier > 10 else multiplier
        return self.request('deauth', {'sta': sta, 'clients': clients, 'multiplier': multiplier, channel: channel})
    def enable(self):
        return self.request('enable')
    def disable(self):
        return self.request('disable')
    def saveSettignsAsDefault(self, config = None):
        if config:
            resp = self.setPineAPSettings(config)
            if (resp['error']):
                return resp
        return self.request('saveAsDefault')