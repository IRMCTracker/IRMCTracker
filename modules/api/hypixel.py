from modules.utils import *

class Hypixel:
    def __init__(self, username=None, uuid=None) -> None:
        if username:
            self.uuid = UsernameToUUID(username).get_uuid()
        elif uuid:
            self.uuid = uuid
    
    def is_valid(self):
        return True if self.uuid != '' else False