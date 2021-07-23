from modules.database import create_tables
from modules.tracker import MCTracker
import matplotlib.pyplot as plt
import datetime

create_tables()

t = MCTracker()
t.fetch_and_sort()

print(t.draw_chart())
