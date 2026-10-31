# AWS EKS + Istio Lab

Laboratório prático de microsserviços na AWS utilizando Amazon EKS,
Istio, Kubernetes Gateway API e Terraform.

## Arquitetura

- Orders API: FastAPI
- Orders Worker: Python
- Mensageria: Amazon SQS
- Banco de dados: Amazon DynamoDB
- Containers: Docker
- Orquestração: Amazon EKS
- Service Mesh: Istio
- Entrada HTTP: Kubernetes Gateway API
- Infraestrutura: Terraform
- Registry: Amazon ECR
- CI/CD: GitHub Actions (planejado)

## Estrutura

- src/: código das aplicações
- terraform/: infraestrutura como código
- kubernetes/: manifests Kubernetes
- tests/: testes automatizados
- docs/: documentação técnica

## Testes locais

Ative o ambiente virtual:

    source .venv/bin/activate

Execute:

    PYTHONPATH=src/orders-api:src/orders-worker/app pytest -v tests/

## Orders API

Documentação:

    http://localhost:8000/docs

Health check:

    http://localhost:8000/health/live

## Segurança

- Não versionar credenciais AWS.
- Não armazenar secrets no código.
- Utilizar IAM com privilégio mínimo.
- Utilizar EKS Pod Identity para acesso das aplicações à AWS.
