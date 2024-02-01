#!/usr/bin/python3
"""
Fabric script based on the file 1-pack_web_static.py that distributes an
archive to the web servers
"""

from invoke import run, task
from os.path import exists

env = {'host_string': '54.167.183.175,100.26.169.40'}

@task
def do_deploy(archive_path):
    """distributes an archive to the web servers"""
    if not exists(archive_path):
        return False

    try:
        file_n = archive_path.split("/")[-1]
        no_ext = file_n.split(".")[0]
        path = "/data/web_static/releases/"
        
        # Upload the archive to /tmp/
        run(f'put {archive_path} /tmp/')

        # Create the release directory
        run(f'mkdir -p {path}{no_ext}/')

        # Extract the archive to the release directory
        run(f'tar -xzf /tmp/{file_n} -C {path}{no_ext}/')

        # Remove the uploaded archive
        run(f'rm /tmp/{file_n}')

        # Move the contents to the parent directory and clean up
        run(f'mv {path}{no_ext}/web_static/* {path}{no_ext}/')
        run(f'rm -rf {path}{no_ext}/web_static')

        # Update the symbolic link to the current release
        run(f'rm -rf /data/web_static/current')
        run(f'ln -s {path}{no_ext}/ /data/web_static/current')

        return True
    except Exception as e:
        print(f"Error: {e}")
        return False
