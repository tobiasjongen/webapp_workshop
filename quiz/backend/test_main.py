from fastapi.testclient import TestClient
import random
from datetime import datetime

from main import app

client = TestClient(app)
random.seed(datetime.now().timestamp())

def test_check_endpoints_exist():
    # assume we have question with difficulty 1 and 3
    resp = client.get("/random_question")
    assert resp.status_code == 200
    resp = client.get("/random_question/1")
    assert resp.status_code == 200
    diff = random.randint(0, 100)
    resp = client.get("/random_question/3")
    assert resp.status_code == 200

def test_valid_json_structure():
    # assume we have question with difficulty 1 and 3
    expected_keys = {"question", "difficulty", "correct", "wrong"}
    respWithoutDiff = client.get("/random_question")
    respWithDiff = client.get("/random_question/1")
    for response in [respWithoutDiff, respWithDiff]:
        json = response.json()
        assert isinstance(json, dict)
        assert set(json.keys()) == expected_keys

def test_random_questions():
    equalAnswers = 0
    for i in range(0,10):
        resp1 = client.get("/random_question")
        resp2 = client.get("/random_question")
        if resp1.json()["question"] == resp2.json()["question"]:
            equalAnswers += 1
    assert equalAnswers < 4 # hopefully unlikely enough

    equalAnswers = 0
    for i in range(0,100): 
        resp1 = client.get("/random_question/1")
        resp2 = client.get("/random_question/1")
        if resp1.json()["question"] == resp2.json()["question"]:
            equalAnswers += 1
    assert equalAnswers < 60 # hopefully unlikely enough

def test_diffiuclty():
    # assume we have question with difficulty 1 and 3
    resp = client.get("/random_question/1")
    assert resp.json()["difficulty"] == 1
    resp = client.get("/random_question/3")
    assert resp.json()["difficulty"] == 3
