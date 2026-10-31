output "orders_queue_url" {
  value = aws_sqs_queue.orders.url
}

output "orders_queue_arn" {
  value = aws_sqs_queue.orders.arn
}

output "orders_dlq_url" {
  value = aws_sqs_queue.orders_dlq.url
}

output "orders_table_name" {
  value = aws_dynamodb_table.orders.name
}

output "orders_table_arn" {
  value = aws_dynamodb_table.orders.arn
}

output "orders_api_iam_policy" {
  value = data.aws_iam_policy_document.orders_api.json
}

output "orders_worker_iam_policy" {
  value = data.aws_iam_policy_document.orders_worker.json
}

output "orders_api_iam_policy_arn" {
  value = aws_iam_policy.orders_api.arn
}

output "orders_worker_iam_policy_arn" {
  value = aws_iam_policy.orders_worker.arn
}

output "orders_api_iam_role_arn" {
  value = aws_iam_role.orders_api.arn
}

output "orders_worker_iam_role_arn" {
  value = aws_iam_role.orders_worker.arn
}
