from fabric.api import *
from fabric.contrib.files import exists
from fabric.operations import *
import time
from contextlib import contextmanager
from fabtools import require
import fabtools
from fabtools.python import virtualenv

env.roledefs = {
    'pi': ['pi@192.168.1.8'],
}

env.project_name = 'pi_tower_lamp'
env.source_dir = '/home/pi/source'
env.release_dir = '%s/%s' % (env.source_dir, env.project_name)


def provision():
    """
    Should only run once when creating a new server,
    Provisions using require and then installs project.
    """
    # update
    sudo('apt-get update', pty=True)
    sudo('apt-get upgrade', pty=True)

    # transfer current release
    transfer_project()


def transfer_project():
    if not exists(env.source_dir):
        # create src directory
        sudo('mkdir %s' % env.source_dir)
    if exists(env.release_dir):
        sudo('rm -rf %s' % env.release_dir)
    sudo('mkdir %s' % env.release_dir)
    with cd(env.release_dir):
        #makes an archive from git using git-archive-all https://github.com/Kentzo/git-archive-all
        local("git-archive-all new_release.tar.gz")
        put("new_release.tar.gz", env.source_dir, use_sudo=True)
        sudo("tar zxf %s/new_release.tar.gz" % env.source_dir)
        local("rm -f new_release.tar.gz")