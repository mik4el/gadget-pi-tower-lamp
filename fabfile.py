from fabric.api import *
from fabric.contrib.files import exists
from fabtools import require
from fabtools.python import virtualenv

env.roledefs = {
    'pi': ['pi@192.168.1.8'],  # requires key based auth on server
}

env.project_name = 'pi_tower_lamp'
env.source_dir = '/home/pi/source'
env.release_dir = '%s/%s' % (env.source_dir, env.project_name)
env.virtualenv = '%s/env' % env.source_dir


def provision():
    """
    Should only run once when creating a new server,
    Provisions using require and then installs project.
    """
    # update and upgrade
    sudo('apt-get --yes --force-yes update', pty=True)
    sudo('apt-get --yes --force-yes upgrade', pty=True)

    # install dependencies
    sudo('apt-get --yes --force-yes install python-dev', pty=True)
    sudo('apt-get --yes --force-yes install libjpeg-dev', pty=True)
    sudo('apt-get --yes --force-yes install git', pty=True)

    # install pi-blaster
    sudo('git clone https://github.com/sarfata/pi-blaster.git')
    with cd('pi-blaster'):
        sudo('make')
        sudo('make install')

    # transfer current release
    transfer_project()

    # install current release
    install_project()


def transfer_project():
    if not exists(env.source_dir):
        # create src directory
        sudo("mkdir %s" % env.source_dir)
    if exists(env.release_dir):
        sudo("rm -rf %s" % env.release_dir)
    sudo("mkdir %s" % env.release_dir)
    with cd(env.release_dir):
        # makes an archive from git using git-archive-all https://github.com/Kentzo/git-archive-all
        local("git-archive-all new_release.tar.gz")
        put("new_release.tar.gz", env.source_dir, use_sudo=True)
        sudo("tar zxf %s/new_release.tar.gz" % env.source_dir)
        # make sure that the dir is owned by pi user
        sudo("chown pi:pi -R %s" % env.release_dir)
        local("rm -f new_release.tar.gz")


def install_project():
    """
    Install python project
    """
    if not exists(env.virtualenv):
        create_virtualenv()
    with cd(env.release_dir):
        with virtualenv(env.virtualenv):
            sudo("pip install -r requirements.txt", pty=True)


def deploy():
    transfer_project()
    install_project()


def run_python(operation):
    with cd(env.release_dir):
        with virtualenv(env.virtualenv):
            sudo("python %s" % operation)


def create_virtualenv():
    """
    Creates virtualenv for project in env.virtualenv dir.
    """
    require.python.virtualenv(env.virtualenv, use_sudo=True)


def setup_supervisord():
    if not exists("/home/pi/logs"):
        sudo("mkdir /home/pi/logs")
    sudo("cp %s/supervisord /etc/init.d/supervisord" % env.release_dir)
    sudo("chmod +x /etc/init.d/supervisord")
    sudo("update-rc.d supervisord defaults")
    with cd(env.release_dir):
        with virtualenv(env.virtualenv):
            sudo("/etc/init.d/supervisord restart")
            sudo("supervisorctl restart pi_tower_lamp")


def restart():
    with cd(env.release_dir):
        with virtualenv(env.virtualenv):
            sudo("supervisorctl start pi_tower_lamp")