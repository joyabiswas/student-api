import pytest
from fastapi.testclient import TestClient
from main import app, students

client = TestClient(app)


@pytest.fixture(autouse=True)
def reset_storage():
    students.clear()

    import main
    main.next_id = 1

    yield


def test_create_student():
    response = client.post(
        "/students",
        json={
            "name": "Alice",
            "id_number": "011221001",
            "gpa": 3.9
        }
    )

    assert response.status_code == 201
    assert response.json()["student"]["name"] == "Alice"


def test_get_all_students():
    client.post(
        "/students",
        json={
            "name": "Bob",
            "id_number": "011221002",
            "gpa": 3.5
        }
    )

    response = client.get("/students")

    assert response.status_code == 200
    assert len(response.json()) == 1


def test_update_student():
    client.post(
        "/students",
        json={
            "name": "Carol",
            "id_number": "011221003",
            "gpa": 3.0
        }
    )

    response = client.put(
        "/students/1",
        json={"gpa": 3.8}
    )

    assert response.status_code == 200
    assert response.json()["gpa"] == 3.8
    assert response.json()["name"] == "Carol"


def test_update_not_found():
    response = client.put(
        "/students/999",
        json={"gpa": 4.0}
    )

    assert response.status_code == 404


def test_delete_student():
    client.post(
        "/students",
        json={
            "name": "Dan",
            "id_number": "011221004",
            "gpa": 2.9
        }
    )

    response = client.delete("/students/1")

    assert response.status_code == 200

    check = client.get("/students")

    assert len(check.json()) == 0