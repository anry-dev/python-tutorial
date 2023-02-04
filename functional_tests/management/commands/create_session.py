from django.conf import settings
from django.contrib import auth
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand


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
    '''src: https://gist.github.com/dbrgn/bae5329e17d2801a041e'''
    User = auth.get_user_model()
    user = User.objects.create(email=email)
    session = SessionStore(None)
    session.clear()
    session.cycle_key()
    session[auth.SESSION_KEY] = user._meta.pk.value_to_string(user)
    session[auth.BACKEND_SESSION_KEY] = 'django.contrib.auth.backends.ModelBackend'
    #session[auth.HASH_SESSION_KEY] = user.get_session_auth_hash()
    session.save()
    return session.session_key
