from xml.dom.minidom import parse

import paramiko

parent_repo = "android_12_base"
projects = []

dom = parse("3588_android_12.xml")
data = dom.documentElement

pjs = data.getElementsByTagName("project")
for pj in pjs:
    pj_path = pj.getAttribute("path")
    pj_name = pj.getAttribute("name")
    pj_groups = pj.getAttribute("groups")

    project = {"name": pj_name}
    projects.append(project)

GERRIT_URL = "192.168.10.100"
GERRIT_SSH_PORT = 29418
USERNAME = "i314q159"

ssh = paramiko.SSHClient()
ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
ssh.connect(GERRIT_URL, port=GERRIT_SSH_PORT, username=USERNAME)


def create_project(name):
    stdin, stdout, stderr = ssh.exec_command(
        f"gerrit create-project {parent_repo}/{name} --empty-commit"
    )

    if stdout.channel.recv_exit_status() != 0:
        print(f"Failed to create project {parent_repo}/{name}")
        return False

    print(f"Created project {parent_repo}/{name}")
    return True


def set_project_parent(name):
    print(f"Setting parent for {name}")

    stdin, stdout, stderr = ssh.exec_command(
        f"gerrit set-project-parent --parent {parent_repo} {parent_repo}/{name}"
    )

    if stdout.channel.recv_exit_status() != 0:
        print(f"Failed to set parent for {parent_repo}/{name}")
        return False

    print(f"Set parent for {parent_repo}/{name}")
    return True


try:
    for project in projects:
        if create_project(project["name"]):
            set_project_parent(project["name"])

        # create_project(project["name"])
        # set_project_parent(project["name"])
        pass

finally:
    ssh.close()
