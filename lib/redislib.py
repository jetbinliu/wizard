# -*-coding: UTF-8-*-

import redis

import redis
from rediscluster import RedisCluster


def main(key):
    startup_nodes = [{"host": "10.1.1.101", "port": "7000"},
                     {"host": "10.1.1.102", "port": "7000"},
                     {"host": "10.1.1.103", "port": "7000"},
                     ]
    try:
        rc = RedisCluster(startup_nodes=startup_nodes, decode_responses=True)
    except Exception as e:
        print("connect error")
        sys.exit(1)

    if rc.exists(key):
        res = rc.incr(key)
    else:
        rc.set(key, 1)
        res = 1
    print(res)

if __name__ == "__main__":
    from multiprocessing import Pool
    while True:
        pool = Pool(8)
        tables = ['fkzdb']*16
        pool.map(main, tables)
        pool.close()
        pool.join()

