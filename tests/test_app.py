import pytest

from app import app


def test_health():
    client = app.test_client()
    response = client.get("/health")
    assert response.status_code == 200
    data = response.get_json()
    assert data["status"] == "healthy"


def test_prediction():
    client = app.test_client()
    response = client.post("/predict", json={"value": 5})
    assert response.status_code == 200
    data = response.get_json()
    assert data["prediction"] == 50


@pytest.mark.parametrize(
    ("value", "expected"),
    [
        (5, 50),
        (0, 0),
        (-3, -30),
        (1.5, 15),
    ],
)
def test_prediction_values(value, expected):
    client = app.test_client()

    response = client.post("/predict", json={"value": value})

    assert response.status_code == 200
    assert response.get_json()["prediction"] == expected
