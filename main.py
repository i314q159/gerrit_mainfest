from xml.dom.minidom import parse

import paramiko


def get_name(xml_path):
    dom = parse(xml_path)
    data = dom.documentElement
    pjs = data.getElementsByTagName("project")
    projects = []
    for pj in pjs:
        pj_name = pj.getAttribute("name")

        project = {"name": pj_name}
        projects.append(project)

    return projects


def create_project(name, parent_name):
    cmd = f"gerrit create-project --empty-commit --branch master --parent {parent_name} {parent_name}/{name}"
    stdin, stdout, stderr = ssh.exec_command(cmd)

    if stdout.channel.recv_exit_status() != 0:
        print(f"failed to create project: {PARENT_NAME}/{name}")
    print(cmd)


def set_project_parent(name, parent_name):
    cmd = f"gerrit set-project-parent --parent {parent_name} {parent_name}/{name}"

    stdin, stdout, stderr = ssh.exec_command(cmd)

    if stdout.channel.recv_exit_status() != 0:
        print(f"failed to set project: {PARENT_NAME}/{name}")
    print(cmd)


if __name__ == "__main__":
    PARENT_NAME = input("parent repo name: ") or f"i314q159"
    XML_PATH = input("manifest xml: ") or f"./default.xml"

    projects = get_name(xml_path=XML_PATH).copy()

    GERRIT_URL = input("gerrit ip: ") or f"192.168.10.100"
    GERRIT_PORT = input("gerrit port: ") or 29418
    USERNAME = input("gerrit user name: ") or f"hewenbo"

    print(f"{USERNAME}@{GERRIT_URL}:{GERRIT_PORT}")

    ssh = paramiko.SSHClient()
    ssh.set_missing_host_key_policy(paramiko.AutoAddPolicy())
    ssh.connect(GERRIT_URL, port=GERRIT_PORT, username=USERNAME)

    try:
        for project in projects:
            create_project(project["name"], parent_name=PARENT_NAME)
            # set_project_parent(project["name"], parent_name=PARENT_NAME)
            pass
    finally:
        ssh.close()
