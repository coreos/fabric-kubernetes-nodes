from fabric.api import *
from fabric.contrib.files import upload_template as _upload_template
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


@task
def update_engine_status():
    """
    Runs 'update_engine_client -status' to get the current status for Container Linux updates.
    """

    run('update_engine_client -status')


@task
def trigger_cl_update():
    """
    Runs 'update_engine_client -check_for_update' to trigger a check for and install a new version of Container Linux.
    """

    sudo('update_engine_client -check_for_update')
    update_engine_status()


@task
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


###
# NTP
###

env.ntp_settings = {
    "enable_fallback_ntp": True,
    "ntp_servers": [
        "0.coreos.pool.ntp.org",
        "1.coreos.pool.ntp.org",
        "2.coreos.pool.ntp.org",
        "3.coreos.pool.ntp.org"
    ],
    "fallback_ntp_servers": [
        "0.pool.ntp.org",
        "1.pool.ntp.org",
        "2.pool.ntp.org",
        "3.pool.ntp.org"
    ]
}


@task
def upload_ntp_config():
    """
    Uploads the template './templates/timesyncd.conf.j2' to '/etc/systemd/timesyncd.conf' on a remote host.
    """
    _upload_template(
        'timesyncd.conf.j2',
        '/etc/systemd/timesyncd.conf',
        context=env.ntp_settings,
        use_jinja=True,
        template_dir='templates',
        use_sudo=True,
        backup=True
    )

    sudo('cat /etc/systemd/timesyncd.conf')


@task
def sync_ntp():
    """
    Runs 'upload_ntp_config', restarts the NTP service ('systemd-timesyncd'), and outputs the status of 'timedatectl'.
    """
    upload_ntp_config()
    sudo('systemctl restart systemd-timesyncd; sleep 5')
    run('systemctl status systemd-timesyncd -l')
    run('timedatectl status')
