class Store:
    def __init__(self, limit = 120):
        self.store = []
        self.limit = limit

    def append(self, value):
        self.store.append(value)
        
        length = len(self.store)
        if length > self.limit:
            self.store = self.store[l-self.limit:]

    def get(self):
        return self.store
        
        
