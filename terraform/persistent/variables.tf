variable "aws_region" {
  description = "AWS region"
  type        = string
  default     = "us-east-1"
}

variable "environment" {
  description = "Environment name"
  type        = string
  default     = "dev"
}

variable "project" {
  description = "Project name"
  type        = string
  default     = "aws-eks-istio-lab"
}

variable "eks_cluster_name" {
  description = "Name of the future EKS cluster"
  type        = string
  default     = "aws-eks-istio-lab-dev"
}
