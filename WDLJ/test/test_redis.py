import redis, time

redis_pool = redis.ConnectionPool(host='47.113.200.109', port=63791)
redis_conn = redis.Redis(connection_pool=redis_pool)
size = redis_conn.dbsize()
print(size)
# url = redis_conn.get('https://f.zhaogang.com/o_w-cc79a7a1b0e24a53a8a545a017ad79ad.jpg')
# print(url)
