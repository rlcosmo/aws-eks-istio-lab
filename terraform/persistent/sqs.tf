resource "aws_sqs_queue" "orders_dlq" {
  name                      = "${var.project}-${var.environment}-orders-eks-dlq"
  message_retention_seconds = 1209600
  sqs_managed_sse_enabled   = true

  tags = {
    Project     = var.project
    Environment = var.environment
    Component   = "orders-worker"
  }
}

resource "aws_sqs_queue" "orders" {
  name                       = "${var.project}-${var.environment}-orders-eks"
  visibility_timeout_seconds = 180
  message_retention_seconds  = 345600
  receive_wait_time_seconds  = 20
  sqs_managed_sse_enabled    = true

  redrive_policy = jsonencode({
    deadLetterTargetArn = aws_sqs_queue.orders_dlq.arn
    maxReceiveCount     = 5
  })

  tags = {
    Project     = var.project
    Environment = var.environment
    Component   = "orders-api"
  }
}
