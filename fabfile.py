from fabric.api import *
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

###
# Container Linux updates
###

def update_engine_status():
    """
    Runs 'update_engine_client -status' to get the current status for Container Linux updates.
    """

    run('update_engine_client -status')


def trigger_cl_update():
    """
    Runs 'update_engine_client -check_for_update' to trigger a check for and install a new version of Container Linux.
    """

    sudo('update_engine_client -check_for_update')
    update_engine_status()


def enable_cl_update(action='enable', update='no'):
    """
    Enable / disable update-engine, and optionally run a Container Linux update.
    Takes parameters - action: [enable|disable], update: [yes|no]
    """

    if action == "enable":
        sudo('systemctl unmask update-engine')
        sudo('systemctl enable update-engine')
        sudo('systemctl start update-engine')

        if update == 'yes':
            trigger_cl_update()
        else:
            update_engine_status()

    elif action == "disable":
        sudo('systemctl mask update-engine')
        sudo('systemctl stop update-engine')
