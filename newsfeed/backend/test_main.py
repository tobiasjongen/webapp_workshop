from fastapi.testclient import TestClient

from main import app

client = TestClient(app)

# ensure that server is not overloaded with tests
responseSchool = client.get("/school")
responseLocal = client.get("/local")
responseGlobal = client.get("/global")

def test_check_endpoints_exist():
    assert responseSchool.status_code == 200
    assert responseLocal.status_code == 200
    assert responseGlobal.status_code == 200

def test_valid_json_structure():
    # TODO: update test if /global added
    expected_keys = {"title", "link", "teaser"}
    for response in [responseSchool, responseLocal]:
        json = response.json()
        assert isinstance(json, list)
        for item in json:
            assert isinstance(item, dict)
            assert set(item.keys()) == expected_keys

def test_contained_data():
    # TODO: update test if /global added
    for response in [responseSchool, responseLocal]:
        json = response.json()
        assert isinstance(json, list)
        for item in json:
            assert item["title"] != ""
            assert item["link"] != ""
