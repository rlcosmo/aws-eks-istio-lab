resource "aws_dynamodb_table" "orders" {
  name         = "${var.project}-${var.environment}-orders-data"
  billing_mode = "PAY_PER_REQUEST"
  hash_key     = "order_id"

  attribute {
    name = "order_id"
    type = "S"
  }

  deletion_protection_enabled = true

  point_in_time_recovery {
    enabled = false
  }

  server_side_encryption {
    enabled = true
  }

  tags = {
    Project     = var.project
    Environment = var.environment
    Component   = "orders-worker"
  }
}
