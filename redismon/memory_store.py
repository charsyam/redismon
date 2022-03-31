class MemoryStore:
    def __init__(self, limit = 120):
        self.store = {}
        self.limit = limit

    def append(self, host, value):
        if host not in self.store:
            self.store[host] = []

        self.store[host].append(value)

        length = len(self.store[host])
        if length > self.limit:
            self.store = self.store[host][length-self.limit:]

    def keys(self):
        return self.store.keys()

    def get(self, host):
        return self.store[host]
