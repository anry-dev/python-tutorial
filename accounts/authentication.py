from accounts.models import User, Token
from django.contrib.auth.backends import BaseBackend

import logging
logger = logging.getLogger(__name__)
logger.debug(f'auth module: {__name__}')

class TokenAuthenticationBackend(BaseBackend):
    '''token based authentication backend'''

    #def authenticate(self, uid=None):
    def authenticate(self, request=None, uid=''):
        '''perform token authentication'''
        logger.debug(f'auth called: {uid}')
        try:
            token = Token.objects.get(uid=uid)
            email = token.email
            token.delete()
            return User.objects.get(email=email)
        except Token.DoesNotExist:
            return None
        except User.DoesNotExist:
            return User.objects.create(email=email)

    def get_user(self, email):
        '''find correct user by email'''
        logger.debug(f'get_user : {email}')
        try:
            return User.objects.get(email=email)
        except User.DoesNotExist:
            return None
