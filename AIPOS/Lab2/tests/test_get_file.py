from fastapi.testclient import TestClient


def test_success_get_file(client: TestClient) -> None:
    file_name = "test.html"

    response = client.get(f"/api/v0/{file_name}")
    assert response.status_code == 200
    assert response.headers["content-type"] == "application/octet-stream"


def test_fail_get_file(client: TestClient) -> None:
    file_name = "wrong.html"

    response = client.get(f"/api/v0/{file_name}")

    assert response.status_code == 404
    assert response.headers["content-type"] == "application/json"
