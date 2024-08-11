class RedisStorage:

    def __init__(self) -> None:
        self.storage = {}
    
    def add(self, key, val):
        self.storage[key] = val
    
    def get(self, key):
        return self.storage.get(key, None)
    
    def get_storage(self):
        return self.storage