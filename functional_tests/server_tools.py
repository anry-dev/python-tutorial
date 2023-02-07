from fabric.api import run
from fabric.context_managers import settings

import logging
logger = logging.getLogger(__name__)

def _get_manage_dot_py(host):
    '''return command line to run manage.py for the site'''
    # doesn't work on remote host with sessions - Sesstion data corrupt
    # because of _email_password was relative path
    return f'~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'
    #return f'cd ~/sites/{host}/source && ~/sites/{host}/virtualenv/bin/python ~/sites/{host}/source/manage.py'

def reset_database(host):
    '''reset database on remote host'''
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{host}'):
        run(f'{manage_dot_py} flush --noinput')

def create_session_on_server(host, email):
    '''create user session on the remote host'''
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{host}'):
        session_key = run(f'{manage_dot_py} create_session {email}')
        return session_key.strip()

def create_token_on_server(host, email):
    '''create auth token on the remote host'''
    manage_dot_py = _get_manage_dot_py(host)
    with settings(host_string=f'{host}'):
        token = run(f'{manage_dot_py} create_token {email}')
        return token.strip()
