from datetime import datetime, timedelta

class RedisValueObj:

    def __init__(self, value, expiry=None) -> None:
        self.value = value
        self.expiry = None

    def set_value(self, value):
        self.value = value
    
    def get_value(self):
        return self.value
    
    def set_expiry_after(self, duration_ms=None):
        if duration_ms:
            self.expiry = datetime.now() + timedelta(milliseconds=duration_ms)
            return self.expiry
        else:
            return None
        
    def get_expiry(self):
        return self.expiry
    
    def is_expired(self):
        return self.expiry and self.expiry<datetime.now()

