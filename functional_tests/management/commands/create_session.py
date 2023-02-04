from django.conf import settings
from django.contrib import auth
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand
from superlist import settings


class Command(BaseCommand):
    '''command runner'''

    def add_arguments(self, parser):
        '''add arguments'''
        parser.add_argument('email')

    def handle(self, *args, **options):
        '''handle'''
        session_key = create_pre_authenticated_session(options['email'])
        self.stdout.write(session_key)

def create_pre_authenticated_session(email):
    '''create pre-authenticated session on the server'''
    '''modified version'''
    User = auth.get_user_model()
    user, _ = User.objects.get_or_create(email=email)
    session = SessionStore(None)
    session.cycle_key()
    session[auth.SESSION_KEY] = user.pk
    session[auth.BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
    session[auth.HASH_SESSION_KEY] = ''
    session.save()
    return session.session_key
