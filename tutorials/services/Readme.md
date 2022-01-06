# Services

Tutorial :

- https://mlinproduction.com/k8s-services/
- https://kubebyexample.com/en/concept/services
- https://matthewpalmer.net/kubernetes-app-developer/articles/service-kubernetes-example-tutorial.html

> A Service enables network access to a set of Pods in Kubernetes.

In the post on Deployment, an application is deployed creating an API on kubernetes cluster. Now, a Kubernetes Service is used to expose this api to the outside cluster and not just internally.

> A service is an abstraction for pods, providing a stable, so called virtual IP (VIP) address. While pods may come and go and with it their IP addresses, a service allows clients to reliably connect to the containers running in the pod using the VIP. The "virtual" in VIP means it is not an actual IP address connected to a network interface, but its purpose is purely to forward traffic to one or more pods. Keeping the mapping between the VIP and the pods up-to-date is the job of [kube-proxy](https://kubernetes.io/docs/admin/kube-proxy/), a process that runs on every node, which queries the API server to learn about new services in the cluster.

Pre-requsities: [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) and [minikube](https://minikube.sigs.k8s.io/docs/start/)

## Creating a Service

Kubernetes resources are easily created, managed and deployed using configuration files. A Deployment is used to keep a set of pods running by creating pods from a template. A Service is used to allow network access to a set of pods.

There are different [`type` property](https://kubernetes.io/docs/concepts/services-networking/service/#publishing-services-service-types) in the Service's spec determines how the service is exposed to the network such as ClusterIP, NodePort, LoadBalancer and ExternalName.

Services and Deployment work together nicely. Both `selector` in Service and Deployment point to same label of pods.

```yaml
apiVersion: v1
kind: Service
metadata:
  name: hello-python-service
spec:
  selector:
    app: hello-python # this must match the labels we set on the pod
  ports:
    - protocol: "TCP" # the network protocol to use with the port
      port: 6000 # port that incoming traffic goes to
      targetPort: 5000 # port on the pod that traffic should be sent to
  type: LoadBalancer # type with which service is exposed

---
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-python-api
spec:
  selector:
    matchLabels:
      app: hello-python # this must match the labels we set on the pod
  replicas: 4 # tells deployment number of identical pods to create
  template:
    metadata:
      labels:
        app: hello-python # labels on the pod
    spec:
      containers:
        - name: hello-python-container
          image: digitalocean/flask-helloworld:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 5000
```

`apiVersion`: specifies the version of [Kubernetes API](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-versioning) used to create Kubernetes object

`kind`: specifies the type of Kubernetes object to create, in this case Service and also Deployment

`spec`: Characteristics of service i.e. how service is expose and which ports are responsible

Create a Service and Deployment from configuration file

```bash
kubectl create -f services.yaml
```

Get the status of the service (Check if `Cluster-IP` is assigned)

```bash
kubectl get services,deployment,pods,rs
```

`LoadBalancer` is type of service used to expose the api but minkube doesn't support it, only cloud providers support this type of service. Solution is to start a tunnel.

```bash
minikube tunnel # in a separare terminal
```

Describe the detailed description of resource

```bash
kubectl describe deployment hello-python-api
kubectl describe services hello-python-service
kubectl describe pods
```

View logs from within the Pod

```bash
kubectl logs <pod name>
```

A Flask service is running on the pods

```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 120-878-303

```

Test the service endpoint by using `ExternalIP`

```bash
# copy external ip of service
kubectl get services hello-python-service
curl -i <EXTERNAL-IP>:6000
```

Output :

```bash
HTTP/1.0 200 OK
Content-Type: text/html; charset=utf-8
Content-Length: 13
Server: Werkzeug/0.16.1 Python/3.8.1
Date: Sat, 25 Dec 2021 06:48:13 GMT

Hello, World!%
```

Delete the Service and Deployment

```bash
kubectl delete -f services.yaml
```
