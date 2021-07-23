import re

import base64
from os.path import isfile
from mcstatus import MinecraftServer

from selenium import webdriver
from selenium.webdriver import ChromeOptions

from modules.database import get_server
from modules.utils import random_string, get_debug_logger

from modules.tracker.meta import ServerMeta

class MCServer:
    def __init__(self, server_name, server_address, server_real_address = None):
        self.server_name = server_name
        self.server_address = server_address
        self.server_real_address = server_real_address
    
        self.server = self.lookup()
        
        self.fetch_status()

    def lookup(self):
        return MinecraftServer.lookup(self.server_address + ':25565')
    
    def fetch_status(self):
        try:
            self.status = self.server.status()
        except:
            self.status = None
        
        return self.status
    
    def get_online_players(self):
        return self.status.players.online if self.status != None else 0
    
    def get_max_players(self):
        return self.status.players.max if self.status != None else 0

    def get_latency(self):
        return self.status.latency if self.status != None else 0

    def get_version(self):
        if self.status != None:
            return re.sub(r'§[A-Za-z1-9]', '', self.status.version.name)
        return None
            


    def get_name(self, shortified=False):
        name = self.server_name

        if shortified:
            return (name[:10] + '..') if len(name) > 10 else name
        return name
    
    def get_favicon_base64(self):
        return self.status.favicon if self.status != None else None

    def get_favicon_path(self):
        if self.status:
            data = str(self.status.favicon).replace('data:image/png;base64,', '')
            imgdata = base64.b64decode(data)
            filename = f"storage/cache/fav-{self.get_name()}.png"

            with open(filename, 'wb') as f:
                    f.write(imgdata)

            return filename
        else:
            return None

    def fetch_server_from_db(self):
        return get_server(self.get_name())

    def get_description(self) -> str:
        return self.status.description if self.status != None else None

    def get_motd(self):
        if self.status == None:
            return None
            
        options = ChromeOptions()
        options.add_experimental_option('excludeSwitches', ['enable-logging'])
        options.add_argument('--headless')
        options.add_argument('--profile-directory=Default') 
        chrome = webdriver.Chrome(options=options)
        
        description = str(self.get_description()).replace('\n', '%newline%')
        url = 'https://devship.ir/RenderMOTD/index.php?name={}&current={}&max={}&motd={}'.format(self.get_name(), self.get_online_players(), self.get_max_players(), description)
        
        chrome.get(url)

        motd_el = chrome.find_element_by_id('server')
        location = motd_el.location
        size = motd_el.size
        
        png = chrome.get_screenshot_as_png()

        chrome.quit()

        from PIL import Image
        from io import BytesIO

        file_path = 'storage/cache/motd-{}'.format(self.get_name() + '.png')
        
        im = Image.open(BytesIO(png))

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        im = im.crop((left, top, right, bottom))
        im.save(file_path)

        return file_path

    def get_meta(self):
        return ServerMeta(self.server_address)