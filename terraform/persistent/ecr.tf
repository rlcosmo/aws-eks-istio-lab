resource "aws_ecr_repository" "orders_api" {
  name                 = "${var.project}-${var.environment}-orders-api"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = false

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Project     = var.project
    Environment = var.environment
    Application = "orders-api"
  }
}

resource "aws_ecr_repository" "orders_worker" {
  name                 = "${var.project}-${var.environment}-orders-worker"
  image_tag_mutability = "IMMUTABLE"
  force_delete         = false

  image_scanning_configuration {
    scan_on_push = true
  }

  encryption_configuration {
    encryption_type = "AES256"
  }

  tags = {
    Project     = var.project
    Environment = var.environment
    Application = "orders-worker"
  }
}
