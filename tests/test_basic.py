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

import dns.resolver

domain='play.comixcraft.ir'

try:
    srvInfo = {}
    srv_records=dns.resolver.query('_minecraft._tcp.'+domain, 'SRV')
    for srv in srv_records:
        srvInfo['weight']   = srv.weight
        srvInfo['host']     = str(srv.target).rstrip('.')
        srvInfo['priority'] = srv.priority
        srvInfo['port']     = srv.port
    address = '{}:{}'.format(srvInfo['host'], srvInfo['port'])
except dns.resolver.NXDOMAIN:
    address = domain

print(address)


