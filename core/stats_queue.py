
from .stats import Stats
import queue

class StatsQueue:
    queue = queue.Queue()

    @classmethod
    def add(cls, stat):
        cls.queue.put(stat)

    @classmethod
    def remove(cls):
        return cls.queue.get()

    @classmethod
    def empty(cls):
        return cls.queue.empty()