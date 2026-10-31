data "aws_caller_identity" "current" {}

data "aws_partition" "current" {}

data "aws_iam_policy_document" "pod_identity_trust" {
  statement {
    effect = "Allow"

    actions = [
      "sts:AssumeRole",
      "sts:TagSession"
    ]

    principals {
      type = "Service"

      identifiers = [
        "pods.eks.amazonaws.com"
      ]
    }

    condition {
      test     = "StringEquals"
      variable = "aws:SourceAccount"

      values = [
        data.aws_caller_identity.current.account_id
      ]
    }

    condition {
      test     = "ArnEquals"
      variable = "aws:SourceArn"

      values = [
        "arn:${data.aws_partition.current.partition}:eks:${var.aws_region}:${data.aws_caller_identity.current.account_id}:cluster/${var.eks_cluster_name}"
      ]
    }
  }
}

resource "aws_iam_role" "orders_api" {
  name               = "${var.project}-${var.environment}-orders-api-role"
  assume_role_policy = data.aws_iam_policy_document.pod_identity_trust.json

  tags = {
    Project     = var.project
    Environment = var.environment
    Application = "orders-api"
  }
}

resource "aws_iam_role" "orders_worker" {
  name               = "${var.project}-${var.environment}-orders-worker-role"
  assume_role_policy = data.aws_iam_policy_document.pod_identity_trust.json

  tags = {
    Project     = var.project
    Environment = var.environment
    Application = "orders-worker"
  }
}

resource "aws_iam_role_policy_attachment" "orders_api" {
  role       = aws_iam_role.orders_api.name
  policy_arn = aws_iam_policy.orders_api.arn
}

resource "aws_iam_role_policy_attachment" "orders_worker" {
  role       = aws_iam_role.orders_worker.name
  policy_arn = aws_iam_policy.orders_worker.arn
}
