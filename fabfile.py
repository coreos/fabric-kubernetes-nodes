from fabric.api import env
import subprocess
import json
import os

addressType = os.getenv('FAB_KUBE_NODE_ADDRESS_TYPE', "ExternalIP")

nodes = json.loads(subprocess.check_output(["kubectl", "get", "nodes", "-o", "json"]))

for n in nodes["items"]:
    nodeAddr = ""
    for a in n["status"]["addresses"]:
        if a["type"] == addressType:
            nodeAddr = a["address"]

    if nodeAddr == "":
        continue

    for l in n["metadata"]["labels"]:
        key = l + "=" + n["metadata"]["labels"][l]
        if not key in env.roledefs:
            env.roledefs[key] = []
        role = env.roledefs[key]
        role.append(nodeAddr)
