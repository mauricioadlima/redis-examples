def test_set_and_get_string(redis_client):
    redis_client.set("key", "hello world")

    value = redis_client.get("key")

    assert value == "hello world"

def test_list_operations(redis_client):
    redis_client.rpush("numbers", 1, 2, 3, 4)
    assert redis_client.lrange("numbers", 0, -1) == ["1", "2", "3", "4"]

    redis_client.lpush("numbers", 0)
    assert redis_client.lrange("numbers", 0, -1) == ["0", "1", "2", "3", "4"]

    redis_client.rpush("numbers", 5)
    assert redis_client.lrange("numbers", 0, -1) == ["0", "1", "2", "3", "4", "5"]

    popped = redis_client.rpop("numbers")
    assert popped == "5"

    popped = redis_client.lpop("numbers")
    assert popped == "0"

    redis_client.ltrim("numbers", 1, 2)
    assert redis_client.lrange("numbers", 0, -1) == ["2", "3"]

    assert redis_client.llen("numbers") == 2

def test_set_operations(redis_client):
    redis_client.sadd("numbers", 1, 2, 3)
    assert set(redis_client.smembers("numbers")) == {"1", "2", "3"}

    redis_client.sadd("numbers", 3, 4)
    assert set(redis_client.smembers("numbers")) == {"1", "2", "3", "4"}

    assert redis_client.sismember("numbers", 3) == True
    removed = redis_client.srem("numbers", 3, 4)
    assert removed == 2
    assert redis_client.sismember("numbers", 3) == False
    assert set(redis_client.smembers("numbers")) == {"1", "2"}

    popped = redis_client.spop("numbers")
    assert popped in {"1", "2"}
    
    assert redis_client.scard("numbers") == 1

def test_hash_operations(redis_client):
    redis_client.hset("user:1", mapping={"name": "Mauricio", "age": "41"})
    assert redis_client.hget("user:1", "name") == "Mauricio"
    assert redis_client.hget("user:1", "age") == "41"

    redis_client.hset("user:1", "city", "SP")
    assert redis_client.hgetall("user:1") == {"name": "Mauricio", "age": "41", "city": "SP"}

    assert redis_client.hexists("user:1", "name") is True
    assert redis_client.hexists("user:1", "salary") is False

    assert redis_client.hlen("user:1") == 3

    deleted = redis_client.hdel("user:1", "age")
    assert deleted == 1
    assert redis_client.hget("user:1", "age") is None

    redis_client.hincrby("user:1", "visits", 1)
    assert redis_client.hget("user:1", "visits") == "1"
    

