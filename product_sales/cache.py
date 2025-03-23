import threading
from datetime import datetime, timedelta
from time import sleep

cache = {}
CACHE_TTL = timedelta(minutes=5)


def get_from_cache(key):
    if key in cache:
        timestamp, value = cache[key]
        cache[key] = (datetime.utcnow(), value)
        return value
    return None


def set_to_cache(key, value):
    cache[key] = (datetime.utcnow(), value)


def clear_expired_cache():
    while True:
        sleep(CACHE_TTL.total_seconds())  # Ждем 5 минут
        now = datetime.utcnow()
        keys_to_delete = [
            key for key, (timestamp, _) in cache.items()
            if now - timestamp >= CACHE_TTL
        ]
        for key in keys_to_delete:
            del cache[key]


# Запускаем поток для очистки кэша
threading.Thread(target=clear_expired_cache, daemon=True).start()
