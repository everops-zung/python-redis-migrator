"""
Copies all keys from the source Redis host to the destination Redis host.
Useful to migrate Redis instances where commands like SLAVEOF and MIGRATE are
restricted (e.g. on Amazon ElastiCache).
The script scans through the keyspace of the given database number and uses
a pipeline of DUMP and RESTORE commands to migrate the keys.
Requires Redis 2.8.0 or higher.
Python requirements:
click
progressbar
redis
"""

import click
from progressbar import ProgressBar
from progressbar.widgets import Percentage, Bar, ETA
import redis
from redis.exceptions import ResponseError
from rediscluster import RedisCluster

@click.command()
@click.argument('srchost')
@click.argument('srchostauth')
@click.argument('srchostport')
@click.argument('dsthost')
@click.argument('dsthostauth')
@click.argument('dsthostport')
@click.option('--source_startup_nodes', '-s', multiple = True, help='Redis source startup nodes')
@click.option('--dest_startup_nodes', '-d', multiple = True, help='Redis dest startup nodes')

@click.option('--db', default=0, help='Redis db number, default 0')
@click.option('--flush', default=False, is_flag=True, help='Delete all keys from destination before migrating')
@click.option('--cluster', default=False, is_flag=True, help='Delete all keys from destination before migrating')

def migrate(srchost, srchostauth, srchostport, dsthost, dsthostauth, dsthostport, source_startup_nodes, dest_startup_nodes, db, flush, cluster):
    if srchost == dsthost:
        print ('Source and destination must be different.')
        return
    if (cluster):
        s_nodes= []
        d_nodes= []
        for node in source_startup_nodes:
            s_nodes.append( {"host": node, "port": str(srchostport) })
        for node in destartup_nodes:
            d_nodes.append( {"host": node, "port": str(dsthostport) })
        source = RedisCluster(startup_nodes=s_nodes, password=srchostauth)
        dest = RedisCluster(startup_nodes=d_nodes, password=dsthostauth)
    else:
        source = redis.Redis(host=srchost, port=srchostport, db=db, password=srchostauth)
        dest = redis.Redis(host=dsthost, port=dsthostport, db=db, password=dsthostauth)

    if flush:
        dest.flushdb()

    size = source.dbsize()

    if size == 0:
        print ('No keys found.')
        return

    progress_widgets = ['%d keys: ' % size, Percentage(), ' ', Bar(), ' ', ETA()]
    pbar = ProgressBar(widgets=progress_widgets, maxval=size).start()

    COUNT = 2000 # scan size

    cnt = 0
    non_existing = 0
    already_existing = 0
    cursor = 0

    while True:
        cursor, keys = source.scan(cursor, count=COUNT)
        pipeline = source.pipeline()
        for key in keys:
            pipeline.pttl(key)
            pipeline.dump(key)
        result = pipeline.execute()

        pipeline = dest.pipeline()

        for key, ttl, data in zip(keys, result[::2], result[1::2]):
            if ttl is None:
                ttl = 0
            if data != None:
                pipeline.restore(key, ttl, data)
            else:
                non_existing += 1

        results = pipeline.execute(False)
        for key, result in zip(keys, results):
            if result != 'OK':
                e = result
                if hasattr(e, 'message') and (e.message == 'BUSYKEY Target key name already exists.' or e.message == 'Target key name is busy.'):
                    already_existing += 1
                else:
                    print (f'Key failed:', {key}, {data}, {result})
                    # raise e
                    pass

        if cursor == 0:
            break

        cnt += len(keys)
        pbar.update(min(size, cnt))

    pbar.finish()
    print (f'Keys disappeared on source during scan:', non_existing)
    print ('Keys already existing on destination:', already_existing)

if __name__ == '__main__':
    migrate()
