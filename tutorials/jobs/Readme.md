# Jobs

Tutorial :

- https://mlinproduction.com/k8s-jobs/
- https://kubebyexample.com/en/concept/jobs
- https://www.magalix.com/blog/kubernetes-jobs-101

A Job is Kubernetes controller, a higher-level abstraction that creates one or more Pods for running batch processes. It is not considered a good practise to deploy Pods directly to perform tasks as in event of failure Naked Pods won't be rescheduled.

> A Job creates one or more Pods and will continue to retry execution of the Pods until a specified number of them successfully terminate. As pods successfully complete, the Job tracks the successful completions. When a specified number of successful completions is reached, the task (ie, Job) is complete. Deleting a Job will clean up the Pods it created. Suspending a Job will delete its active Pods until the Job is resumed again.

Pre-requsities: [kubectl](https://kubernetes.io/docs/tasks/tools/install-kubectl-linux/) and [minikube](https://minikube.sigs.k8s.io/docs/start/)

## Creating a Job

Kubernetes resources are easily created, managed and deployed using configuration files. As with all other Kubernetes config, a Job needs `apiVersion`, `kind`, and `metadata` fields. A Job also needs a [`.spec` section](https://git.k8s.io/community/contributors/devel/sig-architecture/api-conventions.md#spec-and-status). The `.spec.template` is the only required field of the `.spec`. The `.spec.template` is a [pod template](https://kubernetes.io/docs/concepts/workloads/pods/#pod-templates). Only a [`RestartPolicy`](https://kubernetes.io/docs/concepts/workloads/pods/pod-lifecycle/#restart-policy) equal to `Never` or `OnFailure` is allowed.

There are [different scenarios](https://kubernetes.io/docs/concepts/workloads/controllers/job/#job-patterns) for running jobs such as run one task inside job object ("run-once" pattern), multiple jobs, multiple parallel jobs, etc. Jobs use completion and parallelism parameters to control the patterns the pods run through. Job pods can run as a single task, several sequential tasks, or some parallel tasks in which the first task that finishes instructs the rest of the pods to complete and exit.

Job represents the configuration of a single job.

```yaml
apiVersion: batch/v1
kind: Job
metadata:
  name: countdown-job
spec:
  backoffLimit: 4
  template:
    metadata:
      name: countdown
    spec:
      containers:
        - name: counter-container
          image: centos:7
          command:
            - "bin/bash"
            - "-c"
            - "for i in 9 8 7 6 5 4 3 2 1 ; do echo $i ; done"
      restartPolicy: Never
```

`apiVersion`: specifies the version of [Kubernetes API](https://kubernetes.io/docs/concepts/overview/kubernetes-api/#api-versioning) used to create Kubernetes object

`kind`: specifies the type of Kubernetes object to create, in this case `Job`

[metadata](https://kubernetes.io/docs/reference/kubernetes-api/common-definitions/object-meta/#ObjectMeta): Data that helps [uniquely](https://kubernetes.io/docs/concepts/overview/working-with-objects/common-labels/) identify the object

[spec](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/#JobSpec): JobSpec describes how job execution look lilke. The `.spec.template` field is a Pod template that specifies which Pods our Job should create. It has the same schema as a [Pod](https://mlinproduction.com/k8s-pods/), except that’s nested and doesn’t have an **apiVersion** or **kind**.

[status](https://kubernetes.io/docs/reference/kubernetes-api/workload-resources/job-v1/#JobStatus): Current status of a job

Create a Job from configuration file

```bash
kubectl create -f jobs.yaml
```

Get the status of the pod

A job is executed as a pod.

```bash
kubectl get jobs
```

Describe the detailed description of resource

```bash
kubectl describe jobs countdown
```

Unlike most pods, however, the pod spawned by a job does not continue to run, but will instead reach a "Completed" state.

```bash
kubectl describe pods $POD_NAME
kubectl get pods
```

View logs from within the Pod

```bash
kubectl logs $POD_NAME
```

Delete the Job object which will remove all supervised pods

```bash
kubectl delete jobs countdown-job
```

> One limitation of using Jobs for machine learning workloads is that Job objects needs to be created manually. What if we want Jobs to run at specific times? Or what if we want to run some machine learning Jobs periodically on a recurring schedule? In this case, Kubernetes offers us the [CronJob](https://kubernetes.io/docs/concepts/workloads/controllers/cron-jobs/).

Tutorial: https://mlinproduction.com/k8s-cronjobs/
