import os
from courierman.collection import Collection


expected_results = [
401,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
200,
404,
404,
]

def test_collection():
    collection = Collection(os.path.join(
        "../", "samples", "Postman Echo.postman_collection.json"))
    for request, expected_result in zip(collection.requests, expected_results):
        ans = request.execute()
        assert ans.status_code == expected_result, f"Failure in {request.name}"