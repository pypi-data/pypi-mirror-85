# Copyright 2015–2020 Ben Sturmfels
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
import io
import os

import invoke
from jinja2 import Template
from patchwork.files import exists


def transfer_files_git(c, push_to_origin=True):
    if push_to_origin:
        c.local('git push origin {env.branch}'.format(env=c.env))
    c.sudo('mkdir -p {env.project_dir}'.format(env=c.env))
    c.sudo('chown {c.user} {env.project_dir}'.format(c=c, env=c.env))

    with c.cd(c.env.project_dir):
        c.run('git init --quiet')
        c.run('git config receive.denyCurrentBranch ignore')

    c.local("git push {c.user}@{c.host}:{env.project_dir} {env.branch}".format(
        env=c.env,
        c=c,
    ))
    with c.cd(c.env.project_dir):
        c.run("git reset --hard {env.branch} -- ".format(env=c.env))


def init(c):
    """Misc first-time run things."""
    if not exists(c, '{env.project_dir}/env'.format(env=c.env)):
        c.run('touch {env.project_dir}/env'.format(env=c.env))
    media_dir = os.path.join(c.env.project_dir, c.env.media_dir)
    if not exists(c, media_dir):
        c.run('mkdir -p {media_dir}'.format(media_dir=media_dir))


def prepare_virtualenv(c):
    """Initialise a virtualenv and install required Python modules."""

    if not exists(c, c.env.virtualenv):
        c.sudo("mkdir -p $(dirname {env.virtualenv})".format(env=c.env))
        c.sudo('chown {c.user} $(dirname {env.virtualenv})'.format(c=c, env=c.env))

        c.run("{env.python} -m venv --system-site-packages {env.virtualenv}".format(env=c.env))
    with c.cd(c.env.project_dir):
        c.run("{env.virtualenv}/bin/python -m pip install -r {env.requirements}".format(
            env=c.env))


def prepare_django(c, fail_level='WARNING'):
    # Clear all Python bytecode, just in case we've upgraded Python.
    c.sudo('find {env.project_dir} -type d -name __pycache__ -exec rm -rf {{}} +'.format(env=c.env)) # Python 3
    c.sudo('find {env.project_dir} -type f -name \'*.pyc\' -exec rm -rf {{}} +'.format(env=c.env)) # Python 2

    with c.cd(c.env.project_dir):
        with c.prefix('source {env.project_dir}/env'.format(env=c.env)):
            # Test configuration before we attempt to restart the application server.
            fail_level_arg = ''
            if fail_level:
                fail_level_arg = '--fail-level={}'.format(fail_level)
            c.run('{env.virtualenv}/bin/python manage.py check --deploy {fail_level_arg} --settings={env.settings}'.format(
                env=c.env, fail_level_arg=fail_level_arg, user=c.env.app_user))

            # Collect static files.
            c.run('{env.virtualenv}/bin/python manage.py collectstatic --settings={env.settings} -v0 --noinput --clear'.format(
                env=c.env))

            # Migrate.
            #
            # Printing unicode characters during a migration can fail if remote
            # locale is something like "POSIX". Run `locale` to check.
            with c.prefix('LC_ALL=en_AU.utf8'):
                c.run('{env.virtualenv}/bin/python manage.py migrate --settings={env.settings}'.format(
                    env=c.env))


def fix_permissions(c, read=None, read_write=None):
    """Ensure permissions are set correctly to run site as unprivileged user."""

    if read is None:
        read = []

    if read_write is None:
        read_write = []

    # Uploading user owns the files. Web server/app user has access via group.
    # Others have no access.
    c.sudo('chown --recursive {c.user}:{env.app_user} {env.project_dir}'.format(c=c, env=c.env))
    c.sudo('chmod --recursive u=rwX,g=,o= {env.project_dir}'.format(env=c.env))

    # Assume we always need read access to project directory.
    c.sudo('chmod g+rX {env.project_dir}'.format(env=c.env))

    for path in read:
        c.sudo('chmod --recursive g+rX {path}'.format(path=os.path.join(c.env.project_dir, path)))
    for path in read_write:
        c.sudo('chmod --recursive g+rwX {path}'.format(path=os.path.join(c.env.project_dir, path)))


def _sudo_upload_template(c, local_path, remote_path, mode, owner=None, group=None):
    # My hacked up replacement for upload template is permanently sudo and uses
    # full Jinja2 by default (both unlike Fabric 1).
    owner = c.user if owner is None else owner
    group = c.user if group is None else group
    with open(local_path, 'r') as f:
        content = f.read()
    t = Template(content)
    output = t.render(env=c.env, **c.env) # Both env.X and just X.
    m = io.StringIO(output)
    c.put(m, '/tmp/X')
    c.sudo('mv /tmp/X {remote_path}'.format(local_path=local_path, remote_path=remote_path))
    c.sudo('chown {owner}:{group} {remote_path}'.format(
        owner=owner, group=group, mode=mode, remote_path=remote_path))
    c.sudo('chmod {mode} {remote_path}'.format(mode=mode, remote_path=remote_path))


def reload_uwsgi(c):
    _sudo_upload_template(
        c, c.env.uwsgi_conf, '/etc/uwsgi-emperor/vassals/{env.site_name}.ini'.format(env=c.env), '644')

    # Append secrets to uWSGI config on-the-fly.
    #
    # uWSGI config format for environment variables is different to a file
    # you might `source`. It has "env = " at the start instead of export,
    # doesn't mind whitespace in the values and treats quotes literally.
    #
    # See here on getting quotes right https://lists.gnu.org/archive/html/fab-user/2013-01/msg00005.html.
    c.sudo('echo "" >> /etc/uwsgi-emperor/vassals/{env.site_name}.ini'.format(env=c.env))
    c.sudo("""sed 's/export/env =/' {env.project_dir}/env | sed "s/['\\"]//g" >> /etc/uwsgi-emperor/vassals/{env.site_name}.ini""".format(env=c.env))


def flush_memcached(c):
    """Clear cache by restarting the memcached server.

    By design, any user on the system can issue commands to memcached, including
    to flush the whole cache. Alternately, we could install libmemcached-tools
    and run `memcflush --servers localhost`.

    """
    c.run("echo flush_all | nc -w1 localhost 11211")


def update_nginx(c):
    _sudo_upload_template(
        c, c.env.nginx_conf, '/etc/nginx/sites-available/{env.site_name}'.format(env=c.env), '644')
    c.sudo("ln -s --force /etc/nginx/sites-available/{env.site_name} /etc/nginx/sites-enabled/{env.site_name}".format(
            env=c.env))
    c.sudo("/usr/sbin/nginx -t")
    c.sudo("/etc/init.d/nginx force-reload")


def download_postgres_db(c):
    tempfile = c.run('tempfile').stdout.strip()
    c.sudo('pg_dump --format=c {env.db_name} > {tempfile}'.format(
        env=c.env, tempfile=tempfile), user='postgres', pty=True)
    localtempfile = '{env.site_name}-{time:%Y-%m-%dT%H:%M:%S}.dump'.format(
        env=c.env, time=datetime.datetime.now())
    c.get(tempfile, localtempfile)
    # localtempfile = get(tempfile, local_path='%(basename)s')[0]
    c.sudo('rm -f {tempfile}'.format(tempfile=tempfile))
    return localtempfile


def mirror_postgres_db(c):
    localtempfile = download_postgres_db(c)
    c.local('dropdb --if-exists {env.db_name}'.format(env=c.env))
    c.local('createdb {env.db_name}'.format(env=c.env))

    # Using sudo here avoids permission errors relating to extensions.
    #
    # Tried removing the above drop and create and adding --clean --create
    # below, but I get a whole bunch of errors relating to things already being
    # in the database.
    c.local('pg_restore --no-owner --no-privileges --dbname={env.db_name} {localtempfile}'.format(
        env=c.env, localtempfile=localtempfile), warn=True)

    c.local("""psql {env.db_name} -c "update django_site set domain = '127.0.0.1:8000'" """.format(env=c.env), warn=True)
    print('You may want to run:\npython3 -m django createsuperuser --username=admin --email=sysadmin@sturm.com.au')


def mirror_media(c):
    c.local('rsync -avz {c.user}@{c.host}:{env.project_dir}/{env.media_dir}/ {env.media_dir}'.format(
        c=c, env=c.env))


def lint(c):
    """Run Pylint over everything."""

    c.local('python3 -m pylint --rcfile=pylint.conf $(find -path ./node_modules -prune -o -type f -name \'*.py\' -print)')


def grep_for_pdb(c, exclude=None):
    """Check that code doesn't ever call the debugger.

    Doing so in production would lock up worker processes.

    """
    if exclude is None:
        exclude = []
    exclude += ['fabfile.py']
    exclusions = ' '.join(["-path './{}' -prune -o".format(ex) for ex in exclude])
    c.local("! find {exclusions} -name '*.py' -exec grep -n '\\bpdb\\b' {{}} +".format(exclusions=exclusions))


def django_test(c):
    c.local('python3 manage.py test --keepdb')


def check_site_online(c):
    """Perform a basic check so we know immediately if the website is down."""

    # TODO: Is there a better way to make invoke fail loudly?
    try:
        c.run('curl --silent --head {c.env.url} | grep --perl-regexp "^HTTP/.+ 200"'.format(c=c))
    except invoke.UnexpectedExit as c:
        raise invoke.Exit('Site check failed!')


def install_scheduled_jobs(c, periodic_jobs=None, crontabs=None):
    periodic_jobs = [] if periodic_jobs is None else periodic_jobs
    crontabs = [] if crontabs is None else crontabs

    typical_periodic_jobs = {
        'deploy/cron.hourly',
        'deploy/cron.daily',
        'deploy/cron.weekly',
        'deploy/cron.monthly',
    }
    for job in periodic_jobs:
        if job in typical_periodic_jobs:
            basename = os.path.basename(job)
            _sudo_upload_template(
                c,
                job,
                '/etc/{basename}/{env.site_name}'.format(basename=basename, env=c.env),
                '755',
            )
        else:
            raise RuntimeError('Unexpected periodic job: {job}'.format(job=job))
    for crontab in crontabs:
        name = os.path.basename(crontab).replace('cron.', '')
        _sudo_upload_template(
            c,
            crontab,
            '/etc/cron.d/{env.site_name}-{name}'.format(name=name, env=c.env),
            '644',
            'root',
            'root',
        )


def django_shell(c):
    with c.cd(c.env.project_dir):
        c.run('source ./env && DJANGO_SETTINGS_MODULE={env.settings} {env.virtualenv}/bin/python manage.py shell'.format(env=c.env), pty=True)


def bash(c):
    with c.cd(c.env.project_dir):
        c.run('bash', pty=True)
