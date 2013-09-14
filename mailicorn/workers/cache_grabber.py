import memcache

memcache_host = '127.0.0.1:11211'

client = memcache.Client([memcache_host], debug=0)


def get_msg_body(mid):
    return mc.get(mid)
