from collections import OrderedDict, defaultdict


class LRUCache(OrderedDict):
    def __init__(self, capacity):
        self.capacity = capacity
        OrderedDict.__init__(self)

    def getitem(self,  key):
        if key not in OrderedDict.keys(self): return -1
        value = OrderedDict.__getitem__(self, key)
        return self._touchCache(key, value)

    def setitem(self, key, value):
        self._touchCache(key, value)

    def _touchCache(self, key, value):
        try:
            OrderedDict.__delitem__(self, key)
        except KeyError:
            pass
        OrderedDict.__setitem__(self, key, value)
        toDel = len(self) - self.capacity
        if toDel > 0:
                OrderedDict.popitem(self, last=False)
        return value

