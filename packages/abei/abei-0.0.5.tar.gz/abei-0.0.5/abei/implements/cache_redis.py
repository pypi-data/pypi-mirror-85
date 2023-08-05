from redis import WatchError

from abei.interfaces import (
    ICache,
    IService,
    service_entry as _
)


class Cache(ICache):

    def __init__(self, service_site, **kwargs):
        service = service_site.get_service(_(IService, 'redis'))
        self.redis = service.redis
        print("----cache_redis component initialized----")

    def get_value(self, key):
        return self.redis.get(key)

    def set_value(self, key, value, expire):
        return bool(
            self.redis.set(key, value) if expire is None else
            self.redis.setex(key, value, expire)
        )

    def set_value_if_match(self, key, value, match, expire):
        with self.redis.pipeline() as p:
            while True:
                try:
                    p.watch(key)
                    v = p.get(key)
                    if v != match:
                        return False
                    if expire is None:
                        expire = p.ttl(key)
                    p.multi()
                    if expire is None:
                        p.set(key, value)
                    else:
                        p.setex(key, value, expire)
                    p.execute()
                    return True
                except WatchError:
                    continue

    def del_value(self, key):
        return bool(self.redis.delete(key))

    def del_value_if_match(self, key, value):
        with self.redis.pipeline() as p:
            while True:
                try:
                    p.watch(key)
                    v = p.get(key)
                    if v is None:
                        return False
                    if v != value:
                        return False
                    p.multi()
                    p.delete(key)
                    p.execute()
                    return True
                except WatchError:
                    continue

    def swp_value(self, key, value, expire):
        val = self.redis.getset(key, value)
        if expire is not None:
            self.redis.expire(key, expire)
        return val
