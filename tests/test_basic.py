from modules.tracker import MCServer
from modules.database import create_tables
from modules.tracker import MCTracker
import matplotlib.pyplot as plt
import datetime
import json
from selenium import webdriver
import hashlib
from mcstatus import MinecraftServer

create_tables()

s = MCServer('TrexMine', 'play.trexmine.com')
print(s.get_motd())

exit()


# https://minecraft.tools/en/css/img/motd-img.png - default minecraft server image png
# s = MinecraftServer('hub.madcraft.ir')
# print(s.status().favicon)
# t = MCTracker()
# t.fetch_and_sort()


# print(t.draw_chart())


