# Kubernetes

In this exercise, we will introduce Kubernetes. Using Kubernetes deploy fastapi application and monitor this application using `Prometheus` and `Grafana`, following best practices of writing tests and trigger a CI workflow using github actions.

Getting started with Kubernetes: [Tutorial](tutorials/Readme.md)

## Run

### Locally

Test the sentiment classifier model

```bash
docker build -t sentiment -f app/sentiment/Dockerfile.sentiment app/sentiment/
docker run --rm -it sentiment
```

Test the fastapi application

```bash
docker build -t sentiment-fastapi .
docker run -p 8000:8000 -e ENABLE_METRICS=true sentiment-fastapi
docker run -p 8000:8000 -it -v $(pwd):/app --entrypoint bash -e ENABLE_METRICS=true sentiment-fastapi # run tests with pytests
pytest --cov
```

Testing the whole suite (fastapi-prometheus-grafana) locally

```bash
docker-compose up --build
```

FastAPI : `localhost:8000`
Prometheus : `localhost:9090`
Grafana : `localhost:3000`

Inside Grafana, login using user: `admin` and password: `admin`. Go to add your data sources, Select Prometheus and add URL : `http://prometheus:9090`. Now we are ready to create a Grafana Dashboard using various metrics logged by prometheus.

Stop the application (in new terminal)

```bash
docker-compose down
```

### Kubernetes

Deploying application i.e the whole suite using Kubernetes.

Pre-requisities : [minikube](https://minikube.sigs.k8s.io/docs/start/) and [helm](https://helm.sh/docs/intro/install/)

1. Start a minikube cluster.

   ```bash
   minikube start --driver=docker --memory 4g --nodes 2
   ```

2. Create a kubectl namespace and Deploy Prometheus and Grafana using the [community Helm chart](https://github.com/prometheus-community/helm-charts/tree/main/charts/kube-prometheus-stack).

   ```bash
   kubectl create namespace monitoring
   helm repo add prometheus-community https://prometheus-community.github.io/helm-charts
   helm install prometheus-stack prometheus-community/kube-prometheus-stack -n monitoring
   ```

3. Check the status of prometheus-stack and all resources running in namespace `monitoring`.

   ```bash
   kubectl --namespace monitoring get pods -l "release=prometheus-stack"
   kubectl get all -n monitoring
   ```

4. Connect to Prometheus and Grafana

   Prometheus

   `prometheus-prometheus-stack-kube-prom-prometheus-0` is the pod name running prometheus.

   ```bash
   kubectl port-forward -n monitoring prometheus-prometheus-stack-kube-prom-prometheus-0 9090
   ```

   Then access via [http://localhost:9090](http://localhost:9090)

   Grafana

   `prometheus-stack-grafana-59f6d879d9-g4xqp` is the pod name running grafana.

   ```bash
   kubectl port-forward -n monitoring prometheus-stack-grafana-59f6d879d9-g4xqp 3000
   ```

   Then access via [http://localhost:3000](http://localhost:3000) and use the default grafana user:password of admin:prom-operator.

   > This password can be configured in the Helm chart values.yaml file

5. Deploy and create a Service of the fastapi application.

   > Note: In order for Prometheus to scrape metrics from this service, we need to define a ServiceMonitor resource. This resource must have the label release: prometheus-stack in order to be discovered. This is configured in the Prometheus resource spec via the serviceMonitorSelector attribute.

   ```bash
   kubectl create -f kubernetes/sentiment.yaml
   ```

   ```bash
   # in another terminal
   minikube tunnel
   ```

   Get the Cluster-IP for the service.

   ```bash
   kubectl get service sentiment-model-service
   ```

   The application can be accessed at `<CLUSTER-IP>:8000/docs`.

6. Delete all deployed resources.

   ```bash
   kubectl delete -f kubernetes/sentiment.yaml
   helm uninstall prometheus-stack -n monitoring
   ```
