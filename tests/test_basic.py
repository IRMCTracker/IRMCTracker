"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from peewee import DoesNotExist
from modules.database import *
from modules.utils import *
from modules.tracker import MCTracker
from modules.api.hypixel import HypixelPlayer
from modules.api import Player as PlayerAPI
from modules.database import Player as PlayerDB
create_tables()

player_db = PlayerDB.get(PlayerDB.username == 'Diamond_Ali')
hypixel_player = json.loads(player_db.hypixel_data)
print(hypixel_player)
hypixel_status = hypixel_player['status']

exit()
import json
get = PlayerDB.get(PlayerDB.username == 'Alijk')
hdata = str(get.hypixel_data).replace("'",'"')
print(hdata)
mcdata = get.minecraft_data
print(type(json.loads(hdata)))

