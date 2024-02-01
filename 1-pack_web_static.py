#!/usr/bin/python3
"""
Fabric script to generate tgz archive
execute: fab -f 1-pack_web_static.py do_pack
"""

from datetime import datetime
from invoke import run, task

@task
def do_pack():
    """
    making an archive on web_static folder
    """

    time = datetime.now()
    archive = f'web_static_{time.strftime("%Y%m%d%H%M%S")}.tgz'
    run('mkdir -p versions')
    create = run(f'tar -cvzf versions/{archive} web_static')

    if create.failed:
        return None
    else:
        return f'versions/{archive}'

