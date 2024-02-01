#!/usr/bin/python3
'''fcreates and distributes an archive to your web servers, using deploy():
'''

import os
from datetime import datetime
from invoke import run, task, puts, Responder

env = {'host_string': '54.167.183.175,100.26.169.40'}

@task
def do_pack():
    """Archives the static files."""
    if not os.path.isdir("versions"):
        os.mkdir("versions")
    cur_time = datetime.now()
    output = f"versions/web_static_{cur_time.year}{cur_time.month}{cur_time.day}{cur_time.hour}{cur_time.minute}{cur_time.second}.tgz"
    try:
        puts(f"Packing web_static to {output}")
        run(f"tar -cvzf {output} web_static")
        archize_size = os.stat(output).st_size
        puts(f"web_static packed: {output} -> {archize_size} Bytes")
    except Exception:
        output = None
    return output

@task
def do_deploy(archive_path):
    """Deploys the static files to the host servers.
    Args:
        archive_path (str): The path to the archived static files.
    """
    if not os.path.exists(archive_path):
        return False
    file_name = os.path.basename(archive_path)
    folder_name = file_name.replace(".tgz", "")
    folder_path = f"/data/web_static/releases/{folder_name}/"
    success = False
    try:
        put(archive_path, f"/tmp/{file_name}")
        run(f"mkdir -p {folder_path}")
        run(f"tar -xzf /tmp/{file_name} -C {folder_path}")
        run(f"rm -rf /tmp/{file_name}")
        run(f"mv {folder_path}web_static/* {folder_path}")
        run(f"rm -rf {folder_path}web_static")
        run("rm -rf /data/web_static/current")
        run(f"ln -s {folder_path} /data/web_static/current")
        puts('New version is now LIVE!')
        success = True
    except Exception:
        success = False
    return success

@task
def deploy():
    """Archives and deploys the static files to the host servers."""
    archive_path = do_pack()
    return do_deploy(archive_path) if archive_path else False

