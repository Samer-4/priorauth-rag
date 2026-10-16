from fastapi.testclient import TestClient
from src.api import app

client = TestClient(app)

def test_health():
    response = client.get("/health")

    assert response.status_code == 200
    assert response.json() == {"status": "healthy"}


def test_get_cases():
    response = client.get("/cases")

    assert response.status_code == 200
    assert isinstance(response.json(), list)
    assert len(response.json()) == 30


def test_get_case():
    response = client.get("/cases/001")

    assert response.status_code == 200
    assert response.json()["case"] == "case_001"


def test_get_case_findings():
    response = client.get("/cases/001/findings")

    assert response.status_code == 200
    assert len(response.json()) == 3
    assert response.json()[0]["check_name"] == "stage4_consistency"


def test_get_case_not_found():
    response = client.get("/cases/999")

    assert response.status_code == 404
    assert response.json()["detail"] == "Case not found"


def test_get_case_findings_not_found():
    response = client.get("/cases/999/findings")

    assert response.status_code == 404
    assert response.json()["detail"] == "Case not found"


def test_get_case_findings_checkpoint_exists():
    # This test assumes that the checkpoint file for case_001 exists.
    # If it doesn't, this test will fail. Adjust the test case as needed.
    response = client.get("/cases/001/findings")

    assert response.status_code == 200
    assert isinstance(response.json(), list)


def test_get_case_findings_empty():
    response = client.get("/cases/009/findings")

    assert response.status_code == 200
    assert response.json() == []
