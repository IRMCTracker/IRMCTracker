"""test.basic.py
`ONLY` For testings purposes

Can be directly executed via running 'python main.py test' command
"""

from datetime import datetime

from modules.utils.functions import shortified
from modules.database.models.vote import get_top_voted_servers
from modules.database import get_servers_limit

import matplotlib.pyplot as plt

from modules.database import *
from modules.utils import *


create_tables()


