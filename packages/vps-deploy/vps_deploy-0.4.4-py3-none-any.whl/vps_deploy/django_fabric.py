# Copyright 2015-2020 Ben Sturmfels
#
# This program is free software: you can redistribute it and/or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program.  If not, see <http://www.gnu.org/licenses/>.

import datetime

from fabric.api import (
    abort, cd, env, get, hide, local, prefix, run, settings, sudo, task)
from fabric.colors import green
from fabric.contrib.files import exists, upload_template


env.branch = 'master'


@task
def flush_memcached():
    """Clear cache by restarting the memcached server.

    By design, any user on the system can issue commands to memcached, including
    to flush the whole cache. Alternately, we could install libmemcached-tools
    and run `memcflush --servers localhost`.

    """
    run("echo flush_all | nc -w1 localhost 11211")


@task
def init():
    """Misc first-time run things."""
    if not exists('{env.project_dir}/env'.format(env=env)):
        run('touch {env.project_dir}/env'.format(env=env))
    if not exists(env.media_dir):
        run('mkdir -p {env.media_dir}'.format(env=env))

@task
def prepare_django(fail_level='WARNING'):
    with cd(env.project_dir):
        # Clear all Python bytecode, just in case we've upgraded Python.
        sudo('find -type d -name __pycache__ | xargs rm -rf') # Python 3
        sudo("find -type f -name '*.pyc' -print0 | xargs -0 rm -f") # Python 2

        # Test configuration before we attempt to restart the application server.
        fail_level_arg = ''
        if fail_level:
            fail_level_arg = '--fail-level={}'.format(fail_level)
        sudo('{env.virtualenv}/bin/python manage.py check --deploy {fail_level_arg} --settings={env.settings}'.format(
            env=env, fail_level_arg=fail_level_arg, user=env.app_user))

        # Collect static files.
        run('{env.virtualenv}/bin/python manage.py collectstatic --settings={env.settings} -v0 --noinput --clear'.format(
            env=env))

        # Migrate.
        #
        # Printing unicode characters during a migration can fail if remote
        # locale is something like "POSIX". Run `locale` to check.
        with prefix('export LC_ALL=en_AU.utf8'):
            run('{env.virtualenv}/bin/python manage.py migrate --settings={env.settings}'.format(
                env=env))


@task
def prepare_virtualenv():
    """Initialise a virtualenv and install required Python modules."""

    if not exists(env.virtualenv):
        sudo("mkdir -p $(dirname {env.virtualenv})".format(env=env))
        sudo('chown {env.user} $(dirname {env.virtualenv})'.format(env=env))

        run("{env.python} -m venv --system-site-packages {env.virtualenv}".format(env=env))
    with cd(env.project_dir):
        run("{env.virtualenv}/bin/python -m pip install -r {env.requirements}".format(
            env=env))


@task
def reload_uwsgi():
    upload_template(
        '{env.uwsgi_conf}'.format(env=env),
        '/etc/uwsgi-emperor/vassals/{env.site_name}.ini'.format(env=env),
        use_sudo=True, mode=0o644, backup=False)
    # Append secrets to uWSGI config on-the-fly.
    with cd(env.project_dir):
        # uWSGI config format for environment variables is different to a file
        # you might `source`. It has "env = " at the start instead of export,
        # doesn't mind whitespace in the values and treats quotes literally.
        #
        # See here on getting quotes right https://lists.gnu.org/archive/html/fab-user/2013-01/msg00005.html.
        sudo('echo "" >> /etc/uwsgi-emperor/vassals/{env.site_name}.ini'.format(env=env))
        sudo(r"""sed 's/export/env =/' env | sed "s/['\\"]//g" >> /etc/uwsgi-emperor/vassals/{env.site_name}.ini""".format(env=env))


@task
def check_for_local_changes():
    """Check and abort if the remote repository has uncommited changes.

    This can be important when working with systems that allow modification of
    theme templates via a web interface, or clients to like to change the code
    directly.

    """
    with cd(env.project_dir):
        if run('git status --untracked=no --porcelain') != '':
            abort('Live branch has local changes. Please manually inspect '
                  'these with `git diff` and either incorporate or reset them.')


@task
def transfer_files_git(push_to_origin=True):
    if push_to_origin:
        local("git push origin {env.branch}".format(env=env))
    sudo('mkdir -p {env.project_dir}'.format(env=env))
    sudo('chown {env.user} {env.project_dir}'.format(env=env))

    with cd(env.project_dir):
        run('git init --quiet')
        run('git config receive.denyCurrentBranch ignore')
    local("git push {env.user}@{env.host}:{env.project_dir} {env.branch}".format(
            env=env),
          capture=False)
    with cd(env.project_dir):
        run("git reset --hard {env.branch} -- ".format(env=env))


@task
def update_nginx():
    sudo("ln -s --force {env.project_dir}/{env.nginx_conf} /etc/nginx/sites-available/{env.site_name}".format(
            env=env))
    sudo("ln -s --force /etc/nginx/sites-available/{env.site_name} /etc/nginx/sites-enabled/{env.site_name}".format(
            env=env))
    sudo("/usr/sbin/nginx -t")
    sudo("/etc/init.d/nginx force-reload")


@task
def lint():
    """Run Pylint over everything."""

    # Work around Python issue in GNU Guix.
    with prefix('unset PYTHONPATH'):
        local('pylint --rcfile=pylint.conf $(find -path ./node_modules -prune -o -type f -name \'*.py\' -print)')


@task
def grep_for_pdb(exclude=None):
    """Check that code doesn't ever call the debugger.

    Doing so in production would lock up worker processes.

    """
    if exclude is None:
        exclude = []
    exclude += ['fabfile.py']
    exclusions = ' '.join(["-path './{}' -prune -o".format(ex) for ex in exclude])
    local("! find {exclusions} -name '*.py' -exec grep -n '\\bpdb\\b' {{}} +".format(exclusions=exclusions))


@task
def fix_permissions(read=None, read_write=None):
    """Ensure permissions are set correctly to run site as unprivileged user."""

    if read is None:
        read = []

    if read_write is None:
        read_write = []

    # Uploading user owns the files. Web server/app user has access via group.
    # Others have no access.
    with cd(env.project_dir):
        sudo('chown --recursive {env.user}:{env.app_user} .'.format(env=env))
        sudo('chmod --recursive u=rwX,g=,o= .')

        # Assume we always need read access to project directory.
        sudo('chmod g+rX .')

        for path in read:
            sudo('chmod --recursive g+rX {path}'.format(path=path))
        for path in read_write:
            sudo('chmod --recursive g+rwX {path}'.format(path=path))


@task
def migrate():
    with cd(env.project_dir):
        run('{env.virtualenv}/bin/python manage.py migrate --settings={env.settings}'.format(
            env=env))


@task
def download_postgres_db():
    tempfile = run('tempfile')
    sudo('sudo -u postgres pg_dump --format=c {env.db_name} > {tempfile}'.format(
        env=env, tempfile=tempfile))
    localtempfile = '{env.site_name}-{time:%Y-%m-%dT%H:%M:%S}.dump'.format(
        env=env, time=datetime.datetime.now())
    get(tempfile, localtempfile)
    # localtempfile = get(tempfile, local_path='%(basename)s')[0]
    sudo('rm -f {tempfile}'.format(tempfile=tempfile))
    return localtempfile


@task
def mirror_postgres_db():
    localtempfile = download_postgres_db()
    local('dropdb --if-exists {env.db_name}'.format(env=env))
    local('createdb {env.db_name}'.format(env=env))
    with settings(warn_only=True):
        # Using sudo here avoids permission errors relating to extensions.
        local('pg_restore --dbname={env.db_name} {localtempfile}'.format(
            env=env, localtempfile=localtempfile))
    # The wrinkle here when using Fabric under GNU Guix, this command will
    # inherit a PYTHONPATH that isn't meant for it. In this case, it's
    # completely wrong because Fabric is Python 2, but it could also be subtley
    # wrong, which would be harder to track down.
    print(green('You may want to run:\npython manage.py createsuperuser --username=admin --email=sysadmin@sturm.com.au'))


@task
def mirror_media():
    with cd(env.project_dir):
        local('rsync -avz {env.user}@{env.host}:{env.project_dir}/{env.media_dir}/ {env.media_dir}'.format(
            env=env))
