import main
from fastapi.testclient import TestClient

client = TestClient(app=main.app)


def test_read_root():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json() == {"Message": "Hello World"}


def test_greet_name():
    response = client.get("/greet/sarath?age=25")

    assert response.status_code == 200
    assert response.json() == {"message": "Hey sarath, you are 25 years old"}


def test_create_student():
    response = client.post(
        "/create_student", json={"name": "sarath", "age": 25, "roll": 28}
    )

    assert response.status_code == 200
    assert response.json() == {"name": "sarath", "age": 25, "roll": 28}

