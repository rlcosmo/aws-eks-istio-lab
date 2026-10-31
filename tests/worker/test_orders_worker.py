import os
import json

os.environ["AWS_DEFAULT_REGION"] = "us-east-1"
os.environ.pop("AWS_PROFILE", None)
os.environ["SQS_QUEUE_URL"] = "https://example.com/test-queue"
os.environ["DYNAMODB_TABLE"] = "orders-test"

import worker

from botocore.exceptions import ClientError


def create_message():
    return {
        "Body": json.dumps({
            "order_id": "order-test-001",
            "correlation_id": "correlation-test-001",
            "customer_id": "customer-001",
            "items": [
                {"product_id": "product-001", "quantity": 2}
            ],
            "status": "PENDING"
        })
    }


def test_process_message_success(monkeypatch):
    captured = {}

    class FakeTable:
        def put_item(self, **kwargs):
            captured.update(kwargs)

    monkeypatch.setattr(worker, "table", FakeTable())

    worker.process_message(create_message())

    assert captured["Item"]["order_id"] == "order-test-001"
    assert captured["Item"]["correlation_id"] == "correlation-test-001"
    assert "ConditionExpression" in captured


def test_duplicate_order_is_ignored(monkeypatch):
    class FakeTable:
        def put_item(self, **kwargs):
            raise ClientError(
                {
                    "Error": {
                        "Code": "ConditionalCheckFailedException",
                        "Message": "Duplicate order"
                    }
                },
                "PutItem"
            )

    monkeypatch.setattr(worker, "table", FakeTable())

    # Não deve propagar exceção para pedidos duplicados.
    worker.process_message(create_message())


def test_dynamodb_failure_is_propagated(monkeypatch):
    class FakeTable:
        def put_item(self, **kwargs):
            raise ClientError(
                {
                    "Error": {
                        "Code": "ProvisionedThroughputExceededException",
                        "Message": "Temporary failure"
                    }
                },
                "PutItem"
            )

    monkeypatch.setattr(worker, "table", FakeTable())

    try:
        worker.process_message(create_message())
        assert False, "Expected ClientError was not raised"
    except ClientError as error:
        assert error.response["Error"]["Code"] == (
            "ProvisionedThroughputExceededException"
        )
