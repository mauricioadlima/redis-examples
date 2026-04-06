def test_timeseries_logs_range(redis_client):
    key = "logs:requests"

    redis_client.ts().create(key)

    redis_client.ts().add(key, 1, 100)
    redis_client.ts().add(key, 2, 200)
    redis_client.ts().add(key, 3, 300)

    result = redis_client.ts().range(key, 1, 2)
    assert result == [(1, 100.0), (2, 200.0)]

    result = redis_client.ts().range(key, "-", "+")
    assert result == [(1, 100.0), (2, 200.0), (3, 300.0)]

    result = redis_client.ts().revrange(key, "-", "+")
    assert result == [(3, 300.0), (2, 200.0), (1, 100.0)]

    redis_client.ts().madd([(key, 4, 400), (key, 5, 500)])

    result = redis_client.ts().range(key, "-", "+")
    assert result == [
        (1, 100.0),
        (2, 200.0),
        (3, 300.0),
        (4, 400.0),
        (5, 500.0),
    ]

def test_timeseries_aggregations(redis_client):
    key = "logs:requests:agg"

    redis_client.ts().create(key)

    redis_client.ts().add(key, 1, 100)

    redis_client.ts().add(key, 2, 200)
    redis_client.ts().add(key, 3, 300)

    redis_client.ts().add(key, 4, 400)
    redis_client.ts().add(key, 5, 500)

    redis_client.ts().add(key, 6, 600)

    result = redis_client.ts().range(key, "-", "+", aggregation_type="min", bucket_size_msec=2)
    assert result ==[(0, 100.0), (2, 200.0), (4, 400.0), (6, 600.0)]

    result = redis_client.ts().range(key, "-", "+", aggregation_type="max", bucket_size_msec=2)
    assert result ==[(0, 100.0), (2, 300.0), (4, 500.0), (6, 600.0)]

    result = redis_client.ts().range(key, "-", "+", aggregation_type="avg", bucket_size_msec=2)
    assert result ==[(0, 100.0), (2, 250.0), (4, 450.0), (6, 600.0)]

    result = redis_client.ts().range(key, "-", "+", aggregation_type="sum", bucket_size_msec=2)
    assert result ==[(0, 100.0), (2, 500.0), (4, 900.0), (6, 600.0)]

    result = redis_client.ts().range(key, "-", "+", aggregation_type="count", bucket_size_msec=2)
    assert result ==[(0, 1.0), (2, 2.0), (4, 2.0), (6, 1.0)]