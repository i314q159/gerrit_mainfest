from xml.dom.minidom import parse

import paramiko


def create_project(name):
    cmd = f"gerrit create-project --empty-commit -b master {parent_repo}/{name}"
    stdin, stdout, stderr = ssh.exec_command(cmd)

    if stdout.channel.recv_exit_status() != 0:
        print(f"Failed to create project {parent_repo}/{name}")
    print(cmd)


def set_project_parent(name, parent_name):
    cmd = f"gerrit set-project-parent --parent {parent_name} {parent_repo}/{name}"

    stdin, stdout, stderr = ssh.exec_command(cmd)

    if stdout.channel.recv_exit_status() != 0:
        print(f"Failed to set parent for {parent_repo}/{name}")
    print(cmd)


if __name__ == "__main__":
    parent_repo = input("parent repo name: ") or f"test"
    projects = []

    xml_path = input("manifest xml: ") or f"./manifest.xml"
    dom = parse(xml_path)
    data = dom.documentElement

    pjs = data.getElementsByTagName("project")
    for pj in pjs:
        pj_path = pj.getAttribute("path")
        pj_name = pj.getAttribute("name")

        project = {"name": pj_name}
        projects.append(project)

    GERRIT_URL = input("gerrit ip: ") or "127.0.0.1"
    GERRIT_PORT = input("gerrit port: ") or 29418
    USERNAME = input("gerrit user name: ") or "i314q159"

    print(f"{USERNAME}@{GERRIT_URL}:{GERRIT_PORT}")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(GERRIT_URL, port=GERRIT_PORT, username=USERNAME)

    try:
        for project in projects:
            # create_project(project["name"])
            set_project_parent(project["name"], parent_name=parent_repo)
            pass
    finally:
        ssh.close()
