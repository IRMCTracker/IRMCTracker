import socket
from urllib.request import urlopen
import json
import dns.resolver

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

        if self.ip is None:
            try:
                srv_records=dns.resolver.resolve('_minecraft._tcp.'+ self.domain.strip(), 'SRV')
                host = str(srv_records[0].target).rstrip('.')
                self.ip = socket.gethostbyname(host)
            except:
                pass
        
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
