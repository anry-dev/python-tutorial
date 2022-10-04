from fabric.contrib.files import append, exists, sed
from fabric.api import env, local, run, sudo
import random

REPO_URL = 'https://github.com/anry-dev/python-tutorial.git'

def deploy():
    '''разворачивание сайта'''

    site_folder = f'/home/{env.user}/sites/{env.host}'
    source_folder = site_folder + '/source'
    _create_directory_structure_if_necessary(site_folder)
    _get_latest_source(source_folder)
    _update_settings(source_folder, env.host)
    _update_virtualenv(source_folder)
    _update_static_files(source_folder)
    _update_database(source_folder)
    _update_nginx(source_folder)
    _update_systemd(source_folder)

def _create_directory_structure_if_necessary(site_folder):
    '''создать структуру каталога, если нужно'''

    for subfolder in ('database', 'static', 'virtualenv', 'source'):
        run(f'mkdir -p {site_folder}/{subfolder}')

def _get_latest_source(source_folder):
    '''получить самый свежий исходный код'''

    if exists(source_folder + '/.git'):
        run(f'cd {source_folder} && git fetch')
        current_commit = local("git log -n 1 --format=%H", capture=True)
        run(f'cd {source_folder} && git reset --hard {current_commit}')
    else:
        run(f'git clone {REPO_URL} {source_folder}')

def _update_settings(source_folder, site_name):
    '''обновить настройки'''

    settings_path = source_folder + '/superlist/settings.py'
    sed(settings_path, "DEBUG = True", "DEBUG = False")
    sed(settings_path,
        'ALLOWED_HOSTS =.+$',
        f'ALLOWED_HOSTS = ["{site_name}"]'
    )

    secret_key_file = source_folder + '/superlist/secret_key.py'
    if not exists(secret_key_file):
        chars = 'abcdefghijklmnopqrstuvwxyz0123456789!@#$%^&*(-_=+)'
        key = ''.join(random.SystemRandom().choice(chars) for _ in range(50))
        append(secret_key_file, f'SECRET_KEY = "{key}"')
    append(settings_path, '\nfrom .secret_key import SECRET_KEY')

def _update_virtualenv(source_folder):
    '''обновить виртуальную среду'''

    virtualenv_folder = source_folder + '/../virtualenv'
    if not exists(virtualenv_folder + '/bin/pip'):
        run(f'python3 -m venv {virtualenv_folder}')

    run(f'{virtualenv_folder}/bin/pip install -r {source_folder}/requirements.txt')

def _update_static_files(source_folder):
    '''обновить статические файлы'''

    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py collectstatic --noinput'
    )

def _update_database(source_folder):
    '''создать БД'''

    run(
        f'cd {source_folder}'
        ' && ../virtualenv/bin/python manage.py migrate --noinput'
    )

def _update_nginx(source_folder):
    '''update nginx config'''

    nginx_conf = f'/etc/nginx/sites-available/{env.host}.conf'
    sudo(
        f'cd {source_folder}'
        f' && cp deploy_tools/nginx.template.conf {nginx_conf}'
    )
    sed(nginx_conf, "__SITENAME__", env.host, use_sudo=True)
    sed(nginx_conf, "__ROOT__", f'/home/{env.user}', use_sudo=True)
    sudo(f'ln -s {nginx_conf} /etc/nginx/sites-enabled')

def _update_systemd(source_folder):
    '''update systemd config'''

    systemd_unit = f'/etc/systemd/system/gunicorn-{env.host}.service'
    sudo(
        f'cd {source_folder}'
        ' && cp deploy_tools/gunicorn-systemd.template.service {systemd_unit}'
    )
    sed(systemd_unit, "__SITENAME__", env.host, use_sudo=True)
    sed(systemd_unit, "__ROOT__", f'/home/{env.user}', use_sudo=True)
    sed(systemd_unit, "__USER__", env.user, use_sudo=True)
    sudo('systemd reload-daemon')
    sudo(f'systemd start gunicorn-{env.host}.service')
