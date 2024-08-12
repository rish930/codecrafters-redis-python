from .redisValueObj import RedisValueObj

class RedisStorage:

    def __init__(self) -> None:
        self.storage = {}
    
    def add(self, key, val, exp_after_ms: int=None):
        rdo = RedisValueObj(value=val)
        if exp_after_ms:
            rdo.set_expiry_after(exp_after_ms)
        self.storage[key] = rdo
        return rdo
    
    def get(self, key):
        return self.storage.get(key, None)
    
    def get_storage(self):
        return self.storage