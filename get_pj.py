# 修改函数set_project_parent里面的父仓名字，修改xml的相对地址

from xml.dom.minidom import parse

import paramiko


def create_project(name):
    cmd = f"gerrit create-project --empty-commit -b master {parent_repo}/{name}"
    stdin, stdout, stderr = ssh.exec_command(cmd)

    if stdout.channel.recv_exit_status() != 0:
        print(f"Failed to create project {parent_repo}/{name}")
        return False

    print(cmd)
    return True


def set_project_parent(name, parent_name):
    # print(f"Setting parent for {name}")

    cmd = f"gerrit set-project-parent --parent {parent_name} {parent_repo}/{name}"

    stdin, stdout, stderr = ssh.exec_command(cmd)

    if stdout.channel.recv_exit_status() != 0:
        print(f"Failed to set parent for {parent_repo}/{name}")
        return False

    print(cmd)
    return True


if __name__ == "__main__":
    parent_repo = "asu_android_11"
    projects = []

    dom = parse("./manifests/asu_android_11.xml")
    data = dom.documentElement

    pjs = data.getElementsByTagName("project")
    for pj in pjs:
        pj_path = pj.getAttribute("path")
        pj_name = pj.getAttribute("name")
        # pj_groups = pj.getAttribute("groups")

        project = {"name": pj_name}
        projects.append(project)

    GERRIT_URL = "192.168.10.100"
    GERRIT_PORT = 29418
    USERNAME = "hewenbo"

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(GERRIT_URL, port=GERRIT_PORT, username=USERNAME)

    try:
        for project in projects:
            # if create_project(project["name"]):
            #     set_project_parent(project["name"])

            # create_project(project["name"])
            set_project_parent(project["name"], parent_name=parent_repo)
            pass
    finally:
        ssh.close()
