# AWS EKS Istio Lab

## Objetivo

Laboratório de microserviços com AWS, Kubernetes, EKS e Istio.

## Aplicações

### Orders API
- Python
- FastAPI
- REST
- Publicação de pedidos no SQS
- Consulta de pedidos no DynamoDB
- Correlation ID
- Health checks

### Orders Worker
- Python
- boto3
- Consumo assíncrono do SQS
- Persistência no DynamoDB
- Idempotência
- Tratamento de falhas
- Encerramento gracioso

## Fluxo

Cliente -> Orders API -> SQS -> Orders Worker -> DynamoDB

## Segurança planejada

- IAM least privilege
- EKS Pod Identity
- Kubernetes RBAC
- Istio mTLS
- Gateway API
- Políticas de autorização

## Observabilidade planejada

- Logs estruturados
- Correlation ID
- Prometheus
- Grafana
- Kiali
- CloudWatch

## Infraestrutura

- Terraform
- AWS EKS
- Dois worker nodes
- Istio Service Mesh
- AWS Network Load Balancer

## Custos

Nenhum recurso AWS deve ser provisionado sem aprovação explícita.
