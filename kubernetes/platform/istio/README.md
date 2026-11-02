# Istio - AWS EKS Lab

## Ambiente

- Cluster: aws-eks-istio-lab-dev
- Kubernetes: 1.37.1
- Istio: 1.31.3
- Profile: minimal

## Instalação

Baixar a versão fixada:

```bash
curl -L https://istio.io/downloadIstio | \
  ISTIO_VERSION=1.31.3 TARGET_ARCH=x86_64 sh -

cd istio-1.31.3
export PATH="$PWD/bin:$PATH"

istioctl version
```

Instalar no cluster:

```bash
istioctl install --set profile=minimal -y
```

## Validação

```bash
kubectl get pods -n istio-system
kubectl get services -n istio-system
istioctl version
istioctl analyze -A
```

## Injeção automática

Namespaces de aplicações habilitados:

- orders-api
- orders-worker

Consultar labels:

```bash
kubectl get namespaces --show-labels
```

Habilitar em um namespace:

```bash
kubectl label namespace orders-api istio-injection=enabled --overwrite
```

Reiniciar workloads existentes para injetar sidecars:

```bash
kubectl rollout restart deployment/orders-api -n orders-api
```

## Recursos dos sidecars

Para respeitar os limites de recursos do namespace, configurar
as annotations nos templates dos Deployments:

```yaml
sidecar.istio.io/proxyCPU: "50m"
sidecar.istio.io/proxyCPULimit: "250m"
sidecar.istio.io/proxyMemory: "64Mi"
sidecar.istio.io/proxyMemoryLimit: "256Mi"
```

## Observações

- Não versionar o pacote de instalação nem o binário istioctl.
- O diretório local istio-1.31.3 permanece ignorado pelo Git.
- A instalação atual utiliza o profile minimal.
- A configuração de Gateway API, ingress, egress e observabilidade
  será documentada nas respectivas etapas do laboratório.
