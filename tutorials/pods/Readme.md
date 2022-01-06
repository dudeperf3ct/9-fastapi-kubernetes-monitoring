# Pods

Tutorial :

- https://mlinproduction.com/k8s-pods/
- https://kubebyexample.com/en/concept/pods
- https://matthewpalmer.net/kubernetes-app-developer/articles/what-is-a-pod-in-kubernetes.html
- https://medium.com/google-cloud/kubernetes-101-pods-nodes-containers-and-clusters-c1509e409e16

> [Pods](https://kubernetes.io/docs/concepts/workloads/pods/) are the smallest deployable units of computing that you can create and manage in Kubernetes.

Pods contain single container or multipler container that need to work together for the application. Any containers in the same pod will share the same resources and local network. Containers can easily communicate with other containers in the same pod as though they were on the same machine while maintaining a degree of isolation from others.

> Each Pod is meant to run a single instance of a given application. If you want to scale your application horizontally (to provide more overall resources by running more instances), you should use multiple Pods, one for each instance. In Kubernetes, this is typically referred to as replication. Replicated Pods are usually created and managed as a group by a workload resource and its controller.

Pre-requsities: [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) and [minikube](https://minikube.sigs.k8s.io/docs/start/)

## Creating a Pod

Kubernetes resources are easily created, managed and deployed using configuration files. These files specify different configuration such as how much of each resource a container needs when you specify a pod, what resources to use, kind of Kubernetes objects to create, etc and lot many things specific to the object.

PodTemplates are specifications for creating Pods. Below is an example of creating a pod running a python-3.8 container that print a `Hello World!` message.

```yaml
apiVersion: v1
kind: Pod
metadata:
  name: python3-pod
  labels:
    app: python3
spec:
  containers:
    - name: python3-container
      image: python:3.8
      command: ["python3", "-c", 'print("Hello, World!")']
  restartPolicy: Never
```

`apiVersion`: specifies the version of [Kubernetes API](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-versioning) used to create Kubernetes object

`kind`: specifies the type of Kubernetes object to create, in this case `Pod`

[metadata](https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/object-meta/#ObjectMeta): Data that helps [uniquely](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/) identify the object

[spec](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/pod-v1/#PodSpec): Characteristics of object to have (for e.g. docker image you want to run on the object, os of the containers, cpu and memory limitations, ports, etc. )

Create a pod from configuration file

```bash
kubectl create -f pods.yaml
```

Get the status of the pod

```bash
kubectl get pods
```

Describe the detailed description of resource

```bash
kubectl describe pod python3-pod
```

View logs from within the Pod

```bash
kubectl logs python3-pod
```

Delete the Pod

```bash
kubectl delete -f pods.yaml
```
