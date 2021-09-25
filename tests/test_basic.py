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

def draw_pie_chart():
    plt.rcParams['text.color'] = 'white'
    # plt.rcParams['font.size'] = '10'
    # plt.rcParams['font.weight'] = 'bold'

    servers = get_servers_limit(8)

    names = [f"{server.name} [ {server.current_players} ]"  for server in servers]
    players = [server.current_players for server in servers]

    fig, ax = plt.subplots(figsize=(10,8))

    ax.pie(players, explode=(0.1, 0, 0, 0, 0, 0, 0, 0), labels=names, autopct='%1.1f%%',
            shadow=True, startangle=90)
    ax.axis('equal')


    # TODO add title, im commenting it for now because it doesnt look good at all
    # plt.title(f"{to_persian('پلیر های ده سرور برتر ایرانی')} - {get_beautified_dt()}")

    output_file = random_cache_file('png')

    plt.show()

    exit()

    plt.savefig(output_file, transparent=True)

    plt.close(fig)

    return output_file


def draw_pie_chart2():
    import numpy as np

    servers = get_servers_limit(8)

    fig, ax = plt.subplots(figsize=(12, 10), subplot_kw=dict(aspect="equal"))

    names = [server.name  for server in servers]
    players = [server.current_players for server in servers]


    def func(pct, allvals):
        absolute = int(round(pct/100.*np.sum(allvals)))
        return "{:.1f}%\n({:d})".format(pct, absolute)


    wedges, texts, autotexts = ax.pie(players, autopct=lambda pct: func(pct, players),
                                    textprops=dict(color="w"))

    ax.legend(wedges, names,
            title="Servers",
            loc="center left",
            bbox_to_anchor=(1, 0, 0.5, 1))

    plt.setp(autotexts, size=8, weight="bold")

    plt.show()

draw_pie_chart2()
