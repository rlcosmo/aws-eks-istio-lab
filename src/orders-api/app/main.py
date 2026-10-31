import os
import json
import uuid
import logging
from datetime import datetime, timezone

import boto3
from fastapi import FastAPI, HTTPException, Request
from pydantic import BaseModel, Field

logging.basicConfig(level=logging.INFO)
logger = logging.getLogger("orders-api")

session = boto3.Session(
    profile_name=os.getenv("AWS_PROFILE") or None,
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

sqs = session.client("sqs")
dynamodb = session.resource("dynamodb")

QUEUE_URL = os.getenv("SQS_QUEUE_URL")
TABLE_NAME = os.getenv("DYNAMODB_TABLE")

app = FastAPI(
    title="CosmoTech Orders API",
    description="Microservice for order management",
    version="1.1.0"
)


class OrderItem(BaseModel):
    product_id: str
    quantity: int = Field(gt=0)


class OrderRequest(BaseModel):
    customer_id: str
    items: list[OrderItem] = Field(min_length=1)


@app.middleware("http")
async def correlation_middleware(request: Request, call_next):
    correlation_id = request.headers.get("X-Correlation-ID")

    if not correlation_id or len(correlation_id) > 128:
        correlation_id = str(uuid.uuid4())

    request.state.correlation_id = correlation_id

    response = await call_next(request)
    response.headers["X-Correlation-ID"] = correlation_id

    return response


@app.get("/health/live")
def liveness():
    return {"status": "alive"}


@app.get("/health/ready")
def readiness():
    if not QUEUE_URL or not TABLE_NAME:
        raise HTTPException(
            status_code=503,
            detail="AWS resources not configured"
        )

    return {"status": "ready"}


@app.post("/orders", status_code=202)
def create_order(order: OrderRequest, request: Request):
    if not QUEUE_URL:
        raise HTTPException(503, "SQS_QUEUE_URL not configured")

    correlation_id = request.state.correlation_id
    order_id = str(uuid.uuid4())

    message = {
        "order_id": order_id,
        "correlation_id": correlation_id,
        "customer_id": order.customer_id,
        "items": [item.model_dump() for item in order.items],
        "status": "PENDING",
        "created_at": datetime.now(timezone.utc).isoformat()
    }

    try:
        response = sqs.send_message(
            QueueUrl=QUEUE_URL,
            MessageBody=json.dumps(message)
        )

        logger.info(
            "order_accepted order_id=%s correlation_id=%s",
            order_id,
            correlation_id
        )

        return {
            "order_id": order_id,
            "correlation_id": correlation_id,
            "status": "PENDING",
            "message_id": response["MessageId"]
        }

    except Exception:
        logger.exception(
            "order_enqueue_failed correlation_id=%s",
            correlation_id
        )
        raise HTTPException(503, "Unable to enqueue order")


@app.get("/orders/{order_id}")
def get_order(order_id: str):
    if not TABLE_NAME:
        raise HTTPException(503, "DYNAMODB_TABLE not configured")

    try:
        response = dynamodb.Table(TABLE_NAME).get_item(
            Key={"order_id": order_id}
        )

        if "Item" not in response:
            raise HTTPException(404, "Order not found")

        return response["Item"]

    except HTTPException:
        raise
    except Exception:
        logger.exception("order_query_failed order_id=%s", order_id)
        raise HTTPException(503, "Unable to query order")
