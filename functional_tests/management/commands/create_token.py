from django.conf import settings
from django.contrib import auth
from django.contrib.sessions.backends.db import SessionStore
from django.core.management.base import BaseCommand
from superlist import settings

from accounts.models import Token

import logging
logger = logging.getLogger(__name__)

class Command(BaseCommand):
    '''command runner'''

    def add_arguments(self, parser):
        '''add arguments'''
        parser.add_argument('email')

    def handle(self, *args, **options):
        '''handle'''
        token = create_auth_token(options['email'])
        self.stdout.write(token)

def create_auth_token(email):
    '''create token for email'''
    token = Token.objects.create(email=email)
    token.save()
    logger.debug(f'token: {token.uid}')
    return str(token.uid)
