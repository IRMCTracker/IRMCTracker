import datetime
from mcserver import MCTracker
import matplotlib.pyplot as plt

tracker = MCTracker()
tracker.fetch_all()
sorted = tracker.sort_all()

tracker.draw_chart()
