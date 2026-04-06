def test_stream_range(redis_client):
    id1 = redis_client.xadd("mystream", {"name": "Mauricio"})
    id2 = redis_client.xadd("mystream", {"name": "Benicio"})
    id3 = redis_client.xadd("mystream", {"name": "Bruna"})

    assert id1 is not None
    assert id2 is not None
    assert id3 is not None

    entries = redis_client.xrange("mystream", "-", "+")
    assert len(entries) == 3
    assert entries[0][1]["name"] == "Mauricio"
    assert entries[1][1]["name"] == "Benicio"
    assert entries[2][1]["name"] == "Bruna"

    last = redis_client.xrevrange("mystream", "+", "-", count=1)
    assert last[0][1]["name"] == "Bruna"

    length = redis_client.xlen("mystream")
    assert length == 3

    deleted = redis_client.xdel("mystream", id1)
    assert deleted == 1
    assert redis_client.xlen("mystream") == 2

def test_stream_xread(redis_client):
    redis_client.xadd("mystream", {"name": "Mauricio"})
    redis_client.xadd("mystream", {"name": "Benicio"})
    redis_client.xadd("mystream", {"name": "Bruna"})

    result = redis_client.xread({"mystream": "0-0"})

    assert len(result) == 1
    stream_name, messages = result[0]
    assert stream_name == "mystream"

    assert len(messages) == 3
    assert messages[0][1]["name"] == "Mauricio"
    assert messages[1][1]["name"] == "Benicio"
    assert messages[2][1]["name"] == "Bruna"

def test_stream_xreadgroup(redis_client):

    redis_client.xadd("mystream", {"name": "Mauricio"})
    redis_client.xadd("mystream", {"name": "Benicio"})
    redis_client.xadd("mystream", {"name": "Bruna"})

    try:
        redis_client.xgroup_create("mystream", "mygroup", id="0-0", mkstream=True)
    except:
        pass

    messages = redis_client.xreadgroup(
        groupname="mygroup",
        consumername="consumer1",
        streams={"mystream": ">"},
        count=1,
        block=0
    )

    assert len(messages) == 1

    stream_name, msgs = messages[0]
    assert stream_name == "mystream"

    names = []
    for msg_id, data in msgs:
        names.append(data["name"])
        redis_client.xack("mystream", "mygroup", msg_id)

    assert names == ["Mauricio"]