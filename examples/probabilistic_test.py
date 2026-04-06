def test_hyperloglog(redis_client):
    key = "hll:test"

    for i in range(1000):
        redis_client.pfadd(key, f"user{i}")

    for i in range(500):
        redis_client.pfadd(key, f"user{i}")

    count = redis_client.pfcount(key)
    print(count)

    assert 989 <= count <= 1011

def test_bloom_filter(redis_client):
    key = "bf:names"

    redis_client.bf().reserve(key, 0.01, 10)

    redis_client.bf().add(key, "giorgio")
    redis_client.bf().add(key, "mateo")
    redis_client.bf().add(key, "matheus")
    redis_client.bf().add(key, "ana julia")
    redis_client.bf().add(key, "antonela")
    redis_client.bf().add(key, "mayc")

    assert redis_client.bf().exists(key, "mateo") == 1

    assert redis_client.bf().exists(key, "benicio") == 0

def test_cuckoo_filter(redis_client):
    key = "cf:names"

    redis_client.cf().reserve(key, 10)

    redis_client.cf().add(key, "giorgio")
    redis_client.cf().add(key, "mateo")
    redis_client.cf().add(key, "matheus")
    redis_client.cf().add(key, "ana julia")
    redis_client.cf().add(key, "antonela")
    redis_client.cf().add(key, "mayc")

    assert redis_client.cf().exists(key, "mateo") == 1

    redis_client.cf().delete(key, "mateo")

    assert redis_client.cf().exists(key, "mateo") == 0

def test_tdigest(redis_client):
    key = "td:api_latency"

    redis_client.tdigest().create(key, 100)

    latencies = [10, 20, 15, 50, 100, 200, 500, 1000, 1500, 2000]
    redis_client.tdigest().add(key, latencies)

    p50 = redis_client.tdigest().quantile(key, 0.50)
    p90 = redis_client.tdigest().quantile(key, 0.80)
    p99 = redis_client.tdigest().quantile(key, 0.99)

    assert p50 == [200]
    assert p90 == [1500]
    assert p99 == [2000]