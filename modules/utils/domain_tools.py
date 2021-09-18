import socket
from urllib.request import urlopen
import json

class DomainInfo:
    def __init__(self, domain) -> None:
        self.domain = domain
        self._fetch()
    
    def _fetch(self):
        self._fetch_ip()
        self._fetch_country()

    def _fetch_ip(self):
        try:
            self.ip = socket.gethostbyname(self.domain.strip())
        except:
            self.ip = None
    
    def _fetch_country(self):
        try:
            response = urlopen('http://ip-api.com/json/{}'.format(self.ip))
  
            output = json.loads(response.read())

            self.country_code = output['countryCode']
            self.region = "{} {}".format(output['country'], output['regionName'])
        except:
            self.country_code = None
            self.region = None
            
    def get_country_code(self):
        return self.country_code

    def get_region(self):
        return self.region
    
    def get_ip(self):
        return self.ip

    def get_domain(self):
        return self.domain
