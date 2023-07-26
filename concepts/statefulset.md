# StatefulSet

## Definition

In Kubernetes, a `StatefulSet` is a higher-level API object that manages the deployment and scaling of a set of Pods, and provides guarantees about the ordering and uniqueness of these Pods.

Here's a bit more detail about what a `StatefulSet` is:

- **Stable Network Identity:** Each pod in a `StatefulSet` derives its hostname from the name of the `StatefulSet` and the ordinal of the Pod. This naming convention is consistent and sticks with the Pod, regardless of which node it's scheduled to run on. This is particularly useful for applications that rely on a stable network identity.

- **Stable Storage:** `StatefulSets` allow you to use Persistent Volumes that are attached to the Pods in a `StatefulSet` and will stick with the Pod throughout its lifecycle. This feature is important for running stateful applications like databases that need persistent, stable storage.

- **Ordered, Graceful Deployment and Scaling:** When deploying or scaling up/down, `StatefulSets` respect the order based on the ordinal index of the Pods. For instance, when you're deploying a `StatefulSet`, Pod 0 is deployed first and Kubernetes waits until it's running and ready before deploying Pod 1, and so on.

- **Ordered, Graceful Deletion and Termination:** When Pods are being deleted, they are terminated in reverse order, starting with the highest ordinal index. Kubernetes waits until a Pod is successfully terminated before terminating the next one.

- **Ordered, Automated Rolling Updates:** When you update a `StatefulSet`, it updates the Pods in a reverse ordinal order, while ensuring that no two Pods are updating at the same time.

In summary, `StatefulSets` are used when you need more control and guarantees over the deployment process and the handling of the application state. This makes them particularly useful for stateful applications like databases (for example, MongoDB, Cassandra, and Elasticsearch) that require unique network identifiers, stable storage, and ordered, graceful deployment and scaling.

## Example

Sure, one of the most common examples of a stateful application that would benefit from using a StatefulSet is a database. Let's use Apache Cassandra, a distributed NoSQL database, as a specific example.

Cassandra is designed to handle large amounts of data across many commodity servers, providing high availability with no single point of failure. It has specific requirements that make it a good fit for a StatefulSet:

1. **Stable Network Identity:** Each Cassandra node uses a gossip protocol to learn about other nodes in the cluster and share location and state information. For this, each node needs to have a stable network identity. With a StatefulSet, each pod in the set has a stable and predictable hostname.

2. **Stable Storage:** Cassandra stores data on disk. If a pod fails and is rescheduled to another node, it's important that the data remains available. StatefulSets allow you to use Persistent Volumes that are attached to the pods in the set and will stick with the pod, providing the stable storage that Cassandra needs.

3. **Ordered Deployment and Scaling:** When scaling a Cassandra cluster up or down, it's important that nodes join or leave the cluster one at a time. StatefulSets ensure that pods are created and deleted in a specific order.

Here's a simplified example of what a StatefulSet might look like for a Cassandra cluster. This is not a complete example and should not be used as is for a production setup:

```yaml
apiVersion: apps/v1
kind: StatefulSet
metadata:
  name: cassandra
spec:
  serviceName: cassandra
  replicas: 3
  selector:
    matchLabels:
      app: cassandra
  template:
    metadata:
      labels:
        app: cassandra
    spec:
      containers:
      - name: cassandra
        image: cassandra:3.11
        ports:
        - containerPort: 9042
          name: cql
        volumeMounts:
        - name: cassandra-data
          mountPath: /var/lib/cassandra/data
  volumeClaimTemplates:
  - metadata:
      name: cassandra-data
    spec:
      accessModes: [ "ReadWriteOnce" ]
      resources:
        requests:
          storage: 1Gi
```
In this example, each pod in the `StatefulSet` would have a unique identifier (0, 1, 2), its own persistent volume claim, and would be deployed one at a time in order.