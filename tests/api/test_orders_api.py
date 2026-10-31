import json

from fastapi.testclient import TestClient

from app import main

client = TestClient(main.app)


def test_liveness():
    response = client.get("/health/live")

    assert response.status_code == 200
    assert response.json()["status"] == "alive"
    assert response.headers.get("x-correlation-id")


def test_correlation_id_is_preserved():
    correlation_id = "lab-test-001"

    response = client.get(
        "/health/live",
        headers={"X-Correlation-ID": correlation_id}
    )

    assert response.status_code == 200
    assert response.headers["x-correlation-id"] == correlation_id


def test_readiness_without_aws_resources():
    main.QUEUE_URL = None
    main.TABLE_NAME = None

    response = client.get("/health/ready")

    assert response.status_code == 503


def test_reject_order_without_items():
    response = client.post(
        "/orders",
        json={"customer_id": "customer-001", "items": []}
    )

    assert response.status_code == 422


def test_reject_order_with_invalid_quantity():
    response = client.post(
        "/orders",
        json={
            "customer_id": "customer-001",
            "items": [
                {"product_id": "product-001", "quantity": 0}
            ]
        }
    )

    assert response.status_code == 422


def test_create_order(monkeypatch):
    main.QUEUE_URL = "https://example.com/test-queue"

    captured = {}

    def fake_send_message(**kwargs):
        captured.update(kwargs)
        return {"MessageId": "message-test-001"}

    monkeypatch.setattr(main.sqs, "send_message", fake_send_message)

    response = client.post(
        "/orders",
        headers={"X-Correlation-ID": "test-correlation-001"},
        json={
            "customer_id": "customer-001",
            "items": [
                {"product_id": "product-001", "quantity": 2}
            ]
        }
    )

    assert response.status_code == 202

    result = response.json()
    message = json.loads(captured["MessageBody"])

    assert result["status"] == "PENDING"
    assert result["message_id"] == "message-test-001"
    assert result["correlation_id"] == "test-correlation-001"
    assert message["correlation_id"] == "test-correlation-001"
    assert message["customer_id"] == "customer-001"
    assert message["items"][0]["quantity"] == 2
