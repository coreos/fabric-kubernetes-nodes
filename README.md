## Integrating Kubernetes with the Fabric Tool

Kubernetes has a database of nodes in the cluster which can be queried with `kubectl get nodes`. This is a powerful database for automation and integration with existing tools. One powerful tool is the [Fabric SSH utility](http://www.fabfile.org/) which is known as a `fabfile.py`.

```
$ kubectl label node ip-10-0-0-50.us-west-2.compute.internal my-special-label=true
$ fab -u core -R my-special-label=true -- date
[52.26.54.211] Executing task '<remainder>'
[52.26.54.211] run: date
[52.26.54.211] out: Thu Feb 16 06:54:37 UTC 2017
[52.26.54.211] out:
```

Learn more at the [Kubernetes Fabric Kubernetes Node](https://github.com/coreos/fabric-kubernetes-nodes) project.

Using a pre-prepared [Kubernetes fabfile.py](https://raw.githubusercontent.com/coreos/fabric-kubernetes-nodes/master/fabfile.py) you can integrate Kubernetes Nodes and labels with fabric. Here is an example session using this integration:

By default this will use the `ExternalIP` of nodes. If you want to change this to say the `InternalIP` export the environment variable `FAB_KUBE_NODE_ADDRESS_TYPE=InternalIP`.

![Demo of fabric integration](http://i.imgur.com/YYHmvMl.gif)

