from fastapi.testclient import TestClient


def test_success_options_file(client: TestClient) -> None:
    file_name = "test.html"

    response = client.options(f"/api/v0/{file_name}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    assert response.json() == {"allow": ["GET", "OPTIONS"], "exists": True}


def test_fail_options_file(client: TestClient) -> None:
    file_name = "wrong.html"

    response = client.options(f"/api/v0/{file_name}")

    assert response.status_code == 200
    assert response.headers["content-type"] == "application/json"

    assert response.json() == {"allow": ["GET", "OPTIONS"], "exists": False}
