import copy
from collections import abc, defaultdict

from threading import Lock

import pyaware.events


class MemoryStorageElement:
    """
    Time series data memory_storage for a single topic
    """

    def __init__(self):
        self.storage = {}
        self.lock = Lock()

    def update(self, data):
        with self.lock:
            self._update(self.storage, data)

    def _update(self, d, u):
        """
        Patches individual items within nested dictionaries
        :param d: Base dictionary
        :param u: Update dictionary
        :return:
        """
        for k, v in u.items():
            if isinstance(v, abc.Mapping):
                self._update(d.get(k, {}), v)
                d[k] = self._update(d.get(k, {}), v)
            else:
                d[k] = v
        return d

    def pop(self):
        with self.lock:
            results = copy.deepcopy(self.storage)
            self.storage.clear()
            return results

    def peek(self):
        with self.lock:
            results = copy.deepcopy(self.storage)
            return results


@pyaware.events.enable
class MemoryStore:
    def __init__(self):
        self.storage = defaultdict(MemoryStorageElement)

    def update(self, data, topic):
        self.storage[topic].update(data)

    def pop(self, topic):
        return self.storage[topic].pop()

    def peek(self, topic):
        return self.storage[topic].peek()
