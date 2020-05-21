
from ..core.stats_queue import StatsQueue
from ..core.stats import OngoingStats

def process_stats_queue():
    while not StatsQueue.empty():
        stat = StatsQueue.remove()
        print(stat)
    return 30.0

def count_time():
    timeStat = OngoingStats()
    StatsQueue.add(timeStat)

    return 10.0