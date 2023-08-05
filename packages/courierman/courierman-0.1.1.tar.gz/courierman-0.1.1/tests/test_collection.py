import os
from courierman.collection import Collection


def test_collection():
    collection = Collection(os.path.join(
        "../", "samples", "Postman Echo.postman_collection.json"))
    assert collection.name == "Postman Echo"
    assert len(collection.items) == 8


def test_collection_requests():
    collection = Collection(os.path.join(
        "../", "samples", "Postman Echo.postman_collection.json"))
    assert len(collection.requests) == 37
