## Integrating Kubernetes Nodes with the Fabric Tool

Kubernetes has a database of nodes in the cluster which can be queried with `kubectl get nodes`. This is a powerful database for automation and integration with existing tools. One powerful tool is the [Fabric SSH utility](http://www.fabfile.org/) which is known as a `fabfile.py`.

### Getting Started

Install the [Fabric SSH utility](http://www.fabfile.org/) and test it out:

```
$ fab --version
Fabric 1.13.1
```

Git clone this repo and move into the directory

```
git clone https://github.com/coreos/fabric-kubernetes-nodes
cd fabric-kubernetes-nodes
```

Fabric will use the `fabfile.py` from the root of this directory. So now Kubernetes Nodes and labels are integrated directly into fabric! Here is an example session using this integration:

```
$ kubectl label node ip-10-0-0-50.us-west-2.compute.internal my-special-label=true
$ fab -u core -R my-special-label=true -- date
[52.26.54.211] Executing task '<remainder>'
[52.26.54.211] run: date
[52.26.54.211] out: Thu Feb 16 06:54:37 UTC 2017
[52.26.54.211] out:
```

![Demo of fabric integration](http://i.imgur.com/YYHmvMl.gif)

### Bastion or Gateway Hosts

Many configurations of Kubernetes, like [Tectonic](https://coreos.com/tectonic), do not enable direct SSH access to machines in the cluster and instead users must first access gateway or bastion hosts. If the Kubernetes cluster has this configuration add the `--gateway` flag to the command and change the address type to .

```
$ export FAB_KUBE_NODE_ADDRESS_TYPE=InternalIP
$ fab --gateway=W.X.Y.Z -u core -R  failure-domain.beta.kubernetes.io/zone=us-west-2a -- date
[10.0.3.24] Executing task '<remainder>'
[10.0.3.24] run: date
[10.0.3.24] out: Mon May  1 02:50:13 UTC 2017
[10.0.3.24] out:

[10.0.60.15] Executing task '<remainder>'
[10.0.60.15] run: date
[10.0.60.15] out: Mon May  1 02:50:16 UTC 2017
[10.0.60.15] out:


Done.
Disconnect
```

By default the fabfile will use the `ExternalIP` of nodes. However, it can be configured to use any IP address that a Node has available. The example above uses the common `InternalIP` field. To change this to a custom `SpecialIP` export the environment variable `FAB_KUBE_NODE_ADDRESS_TYPE=SpecialIP`.

### FAQ

**Q**: With Kubernetes aren't we living in a post-SSH world?

**A**: Kubernetes does enable a workflow where SSH should be less and less necessary for administering machines but often there is still a need to SSH into machines to gather statistics, debug issues, or repair configuration issues. So, while we hope that years from now machines will never need SSH and one-off debugging this tool is useful for the realities of today.
