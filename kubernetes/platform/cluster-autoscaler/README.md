# Cluster Autoscaler - AWS EKS

## Ambiente

- Cluster: aws-eks-istio-lab-dev
- Kubernetes: 1.37.1
- Cluster Autoscaler: 1.36.1 (experimental)
- Node Group: aws-eks-istio-lab-dev-spot
- Capacity Type: Spot
- Instance Type: c7i-flex.large
- Min nodes: 1
- Max nodes: 3
- AWS Region: us-east-1

## Arquitetura

O Cluster Autoscaler monitora Pods não agendáveis e ajusta
automaticamente a capacidade do EKS Managed Node Group.

A descoberta do Auto Scaling Group utiliza as tags:

- k8s.io/cluster-autoscaler/enabled=true
- k8s.io/cluster-autoscaler/aws-eks-istio-lab-dev=owned

## IAM

Role:
aws-eks-istio-lab-dev-cluster-autoscaler-role

Autenticação:
EKS Pod Identity

Namespace:
kube-system

ServiceAccount:
cluster-autoscaler

A role possui permissões de leitura para descoberta e permissões
de alteração restritas ao Auto Scaling Group do laboratório.

A associação Pod Identity é um recurso AWS independente destes
manifests Kubernetes.

## Instalação / atualização

kubectl apply -f rbac.yaml
kubectl apply -f cluster-autoscaler.yaml

## Validação

kubectl get deployment cluster-autoscaler -n kube-system
kubectl get pods -n kube-system -l app=cluster-autoscaler
kubectl logs -n kube-system deployment/cluster-autoscaler

## Scale-down

O experimento utiliza:

- scale-down-unneeded-time: 5m
- scale-down-delay-after-add: 5m
- scale-down-utilization-threshold: 0.5
- max-scale-down-parallelism: 1

## Compatibilidade

A versão 1.36.1 foi testada experimentalmente com Kubernetes 1.37.1.
Esta combinação não possui compatibilidade oficial garantida.
Não utilizar esta configuração como referência de produção sem
validar uma versão correspondente ao Kubernetes do cluster.
