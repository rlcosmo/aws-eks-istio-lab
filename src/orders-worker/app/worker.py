import os
import json
import time
import signal
import logging

import boto3
from botocore.exceptions import ClientError

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s %(levelname)s %(name)s %(message)s"
)

logger = logging.getLogger("orders-worker")

session = boto3.Session(
    profile_name=os.getenv("AWS_PROFILE") or None,
    region_name=os.getenv("AWS_DEFAULT_REGION", "us-east-1")
)

sqs = session.client("sqs")
dynamodb = session.resource("dynamodb")

QUEUE_URL = os.getenv("SQS_QUEUE_URL")
TABLE_NAME = os.getenv("DYNAMODB_TABLE")

if not QUEUE_URL or not TABLE_NAME:
    raise RuntimeError("SQS_QUEUE_URL and DYNAMODB_TABLE are required")

table = dynamodb.Table(TABLE_NAME)

running = True


def shutdown_handler(signum, frame):
    global running
    logger.info("shutdown_signal_received signal=%s", signum)
    running = False


signal.signal(signal.SIGTERM, shutdown_handler)
signal.signal(signal.SIGINT, shutdown_handler)


def process_message(message):
    order = json.loads(message["Body"])

    try:
        table.put_item(
            Item=order,
            ConditionExpression="attribute_not_exists(order_id)"
        )

        logger.info(
            "order_processed order_id=%s correlation_id=%s",
            order["order_id"],
            order.get("correlation_id")
        )

    except ClientError as error:
        code = error.response["Error"]["Code"]

        if code == "ConditionalCheckFailedException":
            logger.info(
                "duplicate_order_skipped order_id=%s",
                order["order_id"]
            )
        else:
            raise


def run():
    logger.info("orders_worker_started")

    while running:
        try:
            response = sqs.receive_message(
                QueueUrl=QUEUE_URL,
                MaxNumberOfMessages=10,
                WaitTimeSeconds=20,
                VisibilityTimeout=180
            )

            for message in response.get("Messages", []):
                try:
                    process_message(message)

                    sqs.delete_message(
                        QueueUrl=QUEUE_URL,
                        ReceiptHandle=message["ReceiptHandle"]
                    )

                except Exception:
                    logger.exception("message_processing_failed")

        except Exception:
            logger.exception("sqs_receive_failed")
            time.sleep(5)

    logger.info("orders_worker_stopped")


if __name__ == "__main__":
    run()
