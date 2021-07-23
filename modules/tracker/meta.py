from selenium import webdriver
from selenium.webdriver import ChromeOptions
from modules.utils import random_string, get_debug_logger


class ServerMeta:
    def __init__(self, address):
        options = ChromeOptions()
        options.add_argument('--headless')
        options.add_argument('--profile-directory=Default') 
        chrome = webdriver.Chrome(options=options)

        self.address = address
        chrome.get('http://localhost/RenderMOTD/?motd={}'.format(self.address))

        try: 
            self.motd_el = chrome.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr[1]/td[2]/span')
            self.motd_el_location = self.motd_el.location
            self.motd_el_size = self.motd_el.size
        except: 
            self.motd_el_location = None
            self.motd_el_size = None

        try: 
            self.info_el = chrome.find_element_by_xpath('/html/body/div/div[2]/table/tbody/tr[2]/td[2]/span')
            self.info_el_location = self.info_el.location
            self.info_el_size = self.info_el.size
        except: 
            self.info_el_location = None
            self.info_el_size = None

        self.png = chrome.get_screenshot_as_png()
        chrome.quit()

    def random_path(self):
        return 'storage/cache/motd-{}'.format(random_string() + '.png')

    def crop_and_save(self, location, size):
        if location == None or size == None:
            return 'null'

        from PIL import Image
        from io import BytesIO

        file_path = self.random_path()
        
        im = Image.open(BytesIO(self.png))

        left = location['x']
        top = location['y']
        right = location['x'] + size['width']
        bottom = location['y'] + size['height']

        im = im.crop((left, top, right, bottom))
        im.save(file_path)

        return file_path

    def get_motd_path(self):
        path = self.crop_and_save(self.motd_el_location, self.motd_el_size)
        get_debug_logger().debug(path)
        return path

    def get_info_path(self):    
        path = self.crop_and_save(self.info_el_location, self.info_el_size)
        get_debug_logger().debug(path)
        return path