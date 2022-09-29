# python-redis-migrator
this project assists with migrating redis servers using a gist from [migrate-redis.py](https://gist.github.com/kitwalker12/517d99c3835975ad4d1718d28a63553e)

# usage
python3 /migrate-redis.py *srchost srcpassword srcport desthost destpassword destport*

# with docker
Create the network:

docker run -it --network red_cluster -v $PWD:/migrator -w /migrator python python3 migrate-redis.py redis-1 ' ' 6379 redis-<n> ' ' 6379

# Create the redis nodes:

for i in {1..3};do docker run -d -v $PWD/cluster-config.conf:/usr/local/etc/redis/redis.conf --name redis-$i --net redis_cluster redis redis-server /usr/local/etc/redis/redis.conf;done
nodes:
1
2
3

docker run -d -v $PWD/cluster-config.conf:/usr/local/etc/redis/redis.conf --name redis-x --net redis_cluster redis redis-server /usr/local/etc/redis/redis.conf


# Create the redis cluster:
docker run -i --rm --net redis_cluster ruby sh -c '\\n gem install redis \\n && wget http://download.redis.io/redis-stable/src/redis-trib.rb \\n && ruby redis-trib.rb create --replicas 1 172.18.0.2:6379'

# Create redis cluster via redis/redis-stack
docker run -i --rm --net redis_cluster redis/redis-stack sh -c 'redis-cli --cluster create 172.18.0.2:6379 172.18.0.3:6379 172.18.0.4:6379 --cluster-yes'                                                                             
>>> Performing hash slots allocation on 3 nodes...
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
M: 9e1c4bfd5268412c369e12da2e64694baea3d794 172.18.0.2:6379
   slots:[0-5460] (5461 slots) master
M: d1981443675150d3b7b130accf3efab82aa228e4 172.18.0.3:6379
   slots:[5461-10922] (5462 slots) master
M: 0a302d8997b193d2c0b964c4caf7f888688e8fe1 172.18.0.4:6379
   slots:[10923-16383] (5461 slots) master
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join
..
>>> Performing Cluster Check (using node 172.18.0.2:6379)
M: 9e1c4bfd5268412c369e12da2e64694baea3d794 172.18.0.2:6379
   slots:[0-5460] (5461 slots) master
M: d1981443675150d3b7b130accf3efab82aa228e4 172.18.0.3:6379
   slots:[5461-10922] (5462 slots) master
M: 0a302d8997b193d2c0b964c4caf7f888688e8fe1 172.18.0.4:6379
   slots:[10923-16383] (5461 slots) master
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.


Log in and set the PWD:

n = number of nodes

redis-1
config set requirepass p@55w0rD

redis-x
config set requirepass p@55w0rDX

example:
docker exec -it redis-x redis-cli
127.0.0.1:6379> config set requirepass p@55w0rDX

Get IP's:
|⇒  docker inspect -f '{{ (index .NetworkSettings.Networks "redis_cluster").IPAddress }}' redis-1
172.18.0.2
|⇒  docker inspect -f '{{ (index .NetworkSettings.Networks "redis_cluster").IPAddress }}' redis-2
172.18.0.5
|⇒  docker inspect -f '{{ (index .NetworkSettings.Networks "redis_cluster").IPAddress }}' redis-3
172.18.0.6
|⇒  docker inspect -f '{{ (index .NetworkSettings.Networks "redis_cluster").IPAddress }}' redis-4


|⇒  docker inspect -f '{{ (index .NetworkSettings.Networks "redis_cluster").IPAddress }}' redis-x
172.18.0.3


for i in {1..3};do docker inspect -f '{{ (index .NetworkSettings.Networks "redis_cluster").IPAddress }}' redis-$i;done
172.18.0.2
172.18.0.3
172.18.0.4

# Cluster status check
docker exec -it redis-3 redis-cli
127.0.0.1:6379> cluster nodes
NOAUTH Authentication required.
127.0.0.1:6379> auth p@55w0rD
OK
127.0.0.1:6379> cluster nodes
9e1c4bfd5268412c369e12da2e64694baea3d794 172.18.0.2:6379@16379 master - 0 1663788143909 1 connected 0-5460
d1981443675150d3b7b130accf3efab82aa228e4 172.18.0.3:6379@16379 master - 0 1663788143000 2 connected 5461-10922
0a302d8997b193d2c0b964c4caf7f888688e8fe1 172.18.0.4:6379@16379 myself,master - 0 1663788141000 3 connected 10923-16383

# Set some keys
docker exec -it redis-3 redis-cli
127.0.0.1:6379> auth p@55w0rD
OK
127.0.0.1:6379> cluster nodes
9e1c4bfd5268412c369e12da2e64694baea3d794 172.18.0.2:6379@16379 master - 0 1663792083386 1 connected 0-5460
d1981443675150d3b7b130accf3efab82aa228e4 172.18.0.3:6379@16379 master - 0 1663792082874 2 connected 5461-10922
0a302d8997b193d2c0b964c4caf7f888688e8fe1 172.18.0.4:6379@16379 myself,master - 0 1663792081000 3 connected 10923-16383
127.0.0.1:6379> SET mykey "c9cd97e75ee5820996683688048b3f4307db9b7a" 1 3 4 5
(error) ERR syntax error
127.0.0.1:6379> SET mykey "c9cd97e75ee5820996683688048b3f4307db9b7a" 
OK
127.0.0.1:6379> GET mykey
"c9cd97e75ee5820996683688048b3f4307db9b7a"
127.0.0.1:6379> 

OR



# Create the second cluster

for i in {1..3};do docker run -d -v $PWD/cluster-config.conf:/usr/local/etc/redis/redis.conf --name redis-x$i --net redis_cluster redis redis-server /usr/local/etc/redis/redis.conf;done

# Create it's cluster
docker run -i --rm --net redis_cluster redis/redis-stack sh -c 'redis-cli --cluster create 172.18.0.5:6379 172.18.0.6:6379 172.18.0.7:6379 --cluster-yes'
>>> Performing hash slots allocation on 3 nodes...
Master[0] -> Slots 0 - 5460
Master[1] -> Slots 5461 - 10922
Master[2] -> Slots 10923 - 16383
M: 63d2134c1e2c535dd6331c25788b99835b9ce367 172.18.0.5:6379
   slots:[0-5460] (5461 slots) master
M: 8a1ea223125661eda8e277d1e70ff2618109e7f1 172.18.0.6:6379
   slots:[5461-10922] (5462 slots) master
M: f318528ac2cf2bf6abdcea341d8b6c4d67bf8beb 172.18.0.7:6379
   slots:[10923-16383] (5461 slots) master
>>> Nodes configuration updated
>>> Assign a different config epoch to each node
>>> Sending CLUSTER MEET messages to join the cluster
Waiting for the cluster to join

>>> Performing Cluster Check (using node 172.18.0.5:6379)
M: 63d2134c1e2c535dd6331c25788b99835b9ce367 172.18.0.5:6379
   slots:[0-5460] (5461 slots) master
M: 8a1ea223125661eda8e277d1e70ff2618109e7f1 172.18.0.6:6379
   slots:[5461-10922] (5462 slots) master
M: f318528ac2cf2bf6abdcea341d8b6c4d67bf8beb 172.18.0.7:6379
   slots:[10923-16383] (5461 slots) master
[OK] All nodes agree about slots configuration.
>>> Check for open slots...
>>> Check slots coverage...
[OK] All 16384 slots covered.

# Set Password
docker exec -it redis-x1 redis-cli
127.0.0.1:6379> config set requirepass p@55w0rDX
OK
127.0.0.1:6379> 
docker exec -it redis-x2 redis-cli
127.0.0.1:6379> config set requirepass p@55w0rDX
OK
127.0.0.1:6379> 
docker exec -it redis-x3 redis-cli
127.0.0.1:6379> config set requirepass p@55w0rDX
OK

# Check the new cluster

docker exec -it redis-x1 redis-cli
127.0.0.1:6379> AUTH p@55w0rDX
OK
127.0.0.1:6379> cluster nodes
8a1ea223125661eda8e277d1e70ff2618109e7f1 172.18.0.6:6379@16379 master - 0 1663790965560 2 connected 5461-10922
63d2134c1e2c535dd6331c25788b99835b9ce367 172.18.0.5:6379@16379 myself,master - 0 1663790964000 1 connected 0-5460
f318528ac2cf2bf6abdcea341d8b6c4d67bf8beb 172.18.0.7:6379@16379 master - 0 1663790965764 3 connected 10923-16383


Turn up ubuntu docker image and install dependencies:
docker run -itd --network redis_cluster -v $PWD:/app -w /app ubuntu
docker exec -it <container_hash_or_name> sh
apt-get update
apt-get install python3 -y
apt-get install pip -y
python3 -m pip install -r requirements.txt

OR run manually
pip3 install click
pip3 install progressbar
pip3 install redis


async-timeout==4.0.2
click==8.1.3
Deprecated==1.2.13
packaging==21.3
progressbar==2.5
pyparsing==3.0.9
redis==4.3.4
wrapt==1.14.1




python3 migrate-redis.py <srchost> <srcpassword> <srcport> <desthost> <destpassword> <destport>

python3 migrate-redis.py 172.18.0.2 p@55w0rD 6379 172.18.0.3 p@55w0rDX 6379

python3 migrate-redis.py 172.18.0.2 p@55w0rD 6379 172.18.0.3 p@55w0rDX 6379
No keys found.

docker exec -it <container_hash> sh
> python3 migrate-redis.py 172.18.0.4 p@55w0rD 6379 172.18.0.7 p@55w0rDX 6379
Key failed: {b'mykey'} {b'\x00(c9cd97e75ee5820996683688048b3f4307db9b7a\n\x00\x98\xc2\xc4\xdeQ/\x15J'} {ResponseError('Invalid TTL value, must be >= 0')}--
1 keys: 100% |##############################################################################################################################| Time: 0:00:00
Keys disappeared on source during scan: 0
Keys already existing on destination: 0

# Helpful commands
## Flush keys
docker exec -it redis-2 sh  -c "redis-cli -a p@55w0rD flushall"
redis-cli cluster nodes