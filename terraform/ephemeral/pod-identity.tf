data "aws_iam_role" "orders_api" {
  name = "aws-eks-istio-lab-dev-orders-api-role"
}

data "aws_iam_role" "orders_worker" {
  name = "aws-eks-istio-lab-dev-orders-worker-role"
}

resource "aws_eks_pod_identity_association" "orders_api" {
  cluster_name    = var.eks_cluster_name
  namespace       = "orders-api"
  service_account = "orders-api-sa"
  role_arn        = data.aws_iam_role.orders_api.arn
}

resource "aws_eks_pod_identity_association" "orders_worker" {
  cluster_name    = var.eks_cluster_name
  namespace       = "orders-worker"
  service_account = "orders-worker-sa"
  role_arn        = data.aws_iam_role.orders_worker.arn
}
