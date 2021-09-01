import socket
from geolite2 import geolite2

class DomainInfo:
    def __init__(self, domain) -> None:
        self.domain = domain
        self._fetch()
    
    def _fetch(self):
        self._fetch_ip()
        self._fetch_country()

    def _fetch_ip(self):
        self.ip = socket.gethostbyname(self.domain.strip())
    
    def _fetch_country(self):
        try:
            reader = geolite2.reader()      
            output = reader.get(self.ip)
            self.country = output['country']['iso_code']
        except:
            self.country = None
            
    def get_country(self):
        return self.country
    
    def get_ip(self):
        return self.ip

    def get_domain(self):
        return self.domain
