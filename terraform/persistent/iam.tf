data "aws_iam_policy_document" "orders_api" {
  statement {
    sid    = "SendOrdersToQueue"
    effect = "Allow"

    actions = [
      "sqs:SendMessage"
    ]

    resources = [
      aws_sqs_queue.orders.arn
    ]
  }

  statement {
    sid    = "ReadOrdersFromDynamoDB"
    effect = "Allow"

    actions = [
      "dynamodb:GetItem"
    ]

    resources = [
      aws_dynamodb_table.orders.arn
    ]
  }
}

data "aws_iam_policy_document" "orders_worker" {
  statement {
    sid    = "ConsumeOrdersQueue"
    effect = "Allow"

    actions = [
      "sqs:ReceiveMessage",
      "sqs:DeleteMessage"
    ]

    resources = [
      aws_sqs_queue.orders.arn
    ]
  }

  statement {
    sid    = "WriteOrdersToDynamoDB"
    effect = "Allow"

    actions = [
      "dynamodb:PutItem"
    ]

    resources = [
      aws_dynamodb_table.orders.arn
    ]
  }
}

resource "aws_iam_policy" "orders_api" {
  name        = "${var.project}-${var.environment}-orders-api-policy"
  description = "Least privilege policy for Orders API"

  policy = data.aws_iam_policy_document.orders_api.json

  tags = {
    Project     = var.project
    Environment = var.environment
  }
}

resource "aws_iam_policy" "orders_worker" {
  name        = "${var.project}-${var.environment}-orders-worker-policy"
  description = "Least privilege policy for Orders Worker"

  policy = data.aws_iam_policy_document.orders_worker.json

  tags = {
    Project     = var.project
    Environment = var.environment
  }
}
