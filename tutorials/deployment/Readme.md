# Deployments

Tutorial :

- https://mlinproduction.com/k8s-deployments/
- https://kubebyexample.com/en/concept/deployments
- https://matthewpalmer.net/kubernetes-app-developer/articles/kubernetes-deployment-tutorial-example-yaml.html
- https://azure.microsoft.com/en-us/overview/kubernetes-deployment-strategy/

> A deployment is a supervisor for pods, giving you fine-grained control over how and when a new pod version is rolled out as well as rolled back to a previous state.

Once we are ready to serve the predictions of our model to users in realtime, we create a Kubernetes Deployment for the application creating an API.

> A deployment allows you to describe an application’s life cycle, such as which images to use for the app, the number of pods there should be, and the way in which they should be updated.

Pre-requsities: [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) and [minikube](https://minikube.sigs.k8s.io/docs/start/)

## Creating a Deployment

Kubernetes resources are easily created, managed and deployed using configuration files. As with all other Kubernetes config, a Deployment needs `apiVersion`, `kind`, and `metadata` fields. A Deployment also needs a [`.spec` section](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status) similar to Job. The `spec.template` required for both Deployment and Job are `PodTemplateSpec` i.e. both describe the pod that will be created for execution. `replicas` in Deployment tells the deployment to run matching number of pod templates. Jobs on other hand have `parallelism` or `completions` that help parallelizing the task if required. The Pods in Jobs get terminated after completion of task but Pods in Deployment as they are a service needs to be up and running always. `restartPolicy` in Deployment is set to `Always` as opposed to options of `OnFailure` and `Never` in Jobs.

The cool feature about Deployment is `rollout` and `scaling`. Rolling out new model will update the Deployment without any downtime. There are different roll out strategies such as [ramped](https://azure.microsoft.com/en-us/overview/kubernetes-deployment-strategy/), [canary](https://medium.com/google-cloud/kubernetes-canary-deployments-for-mere-mortals-13728ce032fe) and [Blue/Green](https://codefresh.io/kubernetes-tutorial/blue-green-deploy/) deployments and live [A/B testing](http://heidloff.net/article/ab-testing-kubernetes-istio). Deployments can be easily scaled if there is increase in demand with least effort. The Deployment of rollout can be pasued, resumed or roll back to previous state just as easily. A Deployment's rollout is triggered if and only if the Deployment's Pod template (that is, `.spec.template`) is changed, for example if the labels or container images of the template are updated.

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: hello-python-api
spec:
  selector:
    matchLabels:
      app: hello-python
  replicas: 4
  template:
    metadata:
      labels:
        app: hello-python
    spec:
      containers:
        - name: hello-python-container
          image: digitalocean/flask-helloworld:latest
          imagePullPolicy: Always
          ports:
            - containerPort: 5000
```

`apiVersion`: specifies the version of [Kubernetes API](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-versioning) used to create Kubernetes object

`kind`: specifies the type of Kubernetes object to create, in this case `Deployment`

[metadata](https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/object-meta/#ObjectMeta): Data that helps [uniquely](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/) identify the object

[spec](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/deployment-v1/#DeploymentSpec): Specification of the desired behavior of the Deployment.

[status](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/deployment-v1/#DeploymentStatus): Most recently observed status of the Deployment.

Create a Deployment from configuration file

```bash
kubectl create -f deployment.yaml
```

Get the status of the deployment

```bash
kubectl get deployments
```

Describe the detailed description of resource

```bash
kubectl describe deployments hello-python-api
```

Keep checking until all 4 pods have their STATUS : Running.

> It’s worth mentioning that the Deployment resource doesn’t manage Pods directly. Instead, the Deployment created a [ReplicaSet](https://kubernetes.io/docs/concepts/workloads/controllers/replicaset/) whose purpose is to maintain a stable set of replica Pods at any given time. The ReplicaSet is used to guarantee the availability of a specific number of identical Pods.

```bash
kubectl get pods
kubectl get rs
```

View logs from within the Pod

```bash
kubectl logs $POD_NAME
```

A Flask App is running in the pods

```bash
 * Serving Flask app "app" (lazy loading)
 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: on
 * Running on http://0.0.0.0:5000/ (Press CTRL+C to quit)
 * Restarting with stat
 * Debugger is active!
 * Debugger PIN: 206-877-587

```

To send a curl request to the flask server running inside the pods, we create a new pod

```bash
kubectl run python3 -ti --image=python:3.8 --command=true bash
```

and inside pod, we run

```bash
curl -i <pod-ip>:5000    # get the pod IP from kubectl describe pods <any-of-4-pod-name> in the IP section
```

A lot many things can be performed on this deployment such as rolling out new update, scaling up the replicas, rolling back the deployment.

Scaling

There are different approaches for scaling the deployment

```bash
kubectl scale --replicas=5 deployment hello-python-api
# check the number of new pods created and their status
kubectl get pods
```

Updating the image : This requires setting `imagePullPolicy` to `Always` before deploying the application to keep rolling out new updates. Once rollout is successful, we get the message of `deployment "hello-python-api" successfully rolled out`.

```bash
kubectl set image deployment/hello-python-api hello-python-container=<new image>
# check the status of rollout
kubectl rollout status deployment hello-python-api
# check the status of replicas and pods
kubectl get rs,pods
# check the rollout history
kubectl rollout history deployment hello-python-api
# check details of specific revision
kubectl rollout history deployment hello-python-api --revision=1
# roll back to previous revision
kubectl rollout undo deployment hello-python-api --to-revision=2
```

Delete the Deployment object which will remove all supervised pods

```bash
kubectl delete -f deployment.yaml
```

Resource : https://kubernetes.io/docs/concepts/workloads/controllers/deployment/
