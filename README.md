# python-redis-migrator
this project assists with migrating redis servers using a gist from [migrate-redis.py](https://gist.github.com/kitwalker12/517d99c3835975ad4d1718d28a63553e)

# usage
python2 /migrate-redis.py <srchost> <srcpassword> <srcport> <desthost> <destpassword> <destport>

# with docker
Create the network:

docker run -it --network red_cluster -v $PWD:/migrator -w /migrator python python3 migrate-redis.py redis-1 ' ' 6379 redis-<n> ' ' 6379

Create the redis nodes:
docker run -d -v $PWD/cluster-config.conf:/usr/local/etc/redis/redis.conf --name redis-x --net redis_cluster redis redis-server /usr/local/etc/redis/redis.conf

Create the redis cluster:
docker run -i --rm --net redis_cluster ruby sh -c '\\n gem install redis \\n && wget http://download.redis.io/redis-stable/src/redis-trib.rb \\n && ruby redis-trib.rb create --replicas 1 172.18.0.2:6379'


Log in and set the PWD:

n = number of nodes

redis-1
config set requirepass p@55w0rD

redis-x
config set requirepass p@55w0rDX

example:
docker exec -it redis-x redis-cli
127.0.0.1:6379> config set requirepass p@55w0rDX

Check IP's:
|⇒  docker inspect -f '{{ (index .NetworkSettings.Networks "redis_cluster").IPAddress }}' redis-1
172.18.0.2
|⇒  docker inspect -f '{{ (index .NetworkSettings.Networks "redis_cluster").IPAddress }}' redis-x
172.18.0.3

Turn up ubuntu docker image and install dependencies:
docker run -itd --network redis_cluster -v $PWD:/app -w /app ubuntu
docker exec -it <container_hash_or_name> sh
apt-get update
apt-get install python3
apt-get install pip -y
pip3 install click
pip3 install progressbar
pip3 install redis
pip freeze

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

# python3 migrate-redis.py 172.18.0.2 p@55w0rD 6379 172.18.0.3 p@55w0rDX 6379
No keys found.