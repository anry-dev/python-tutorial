from django.test import TestCase
from django.contrib import auth
from unittest import skip
from unittest.mock import patch, call
from accounts.models import Token
from accounts.authentication import TokenAuthenticationBackend

User = auth.get_user_model()

class DirectAuthenticationTest(TestCase):
    '''testing direct calls to authentication backend'''

    def test_returns_None_if_no_such_token(self):
        '''test: auth of bad token returns None'''
        result = TokenAuthenticationBackend().authenticate(
                uid='no-such-token'
        )
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        '''test: auth of correct token returns new user with correct email'''
        email = 'token-test@a.bc'
        token = Token.objects.create(email=email)
        user = TokenAuthenticationBackend().authenticate(uid=token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_existing_user_with_correct_email_if_token_exists(self):
        '''test: auth of correct token returns __existing__ user with correct email'''
        email = 'existing-test@a.bc'
        existing_user = User.objects.create(email=email)
        token = Token.objects.create(email=email)
        user = TokenAuthenticationBackend().authenticate(uid=token.uid)
        self.assertEqual(user, existing_user)

    def test_gets_user_by_email(self):
        '''test: get correct user by his email'''
        User.objects.create(email='some-email@a.b')
        email = 'desired-email@a.com'
        desired_user = User.objects.create(email=email)
        user = TokenAuthenticationBackend().get_user(email)
        self.assertEqual(user, desired_user)

    def test_returns_None_if_no_user_with_such_email(self):
        '''test: get_user returns None if no such user'''
        User.objects.create(email='some-email@a.b')
        email = 'no-such-user-email@a.com'
        user = TokenAuthenticationBackend().get_user(email)
        self.assertIsNone(user)

    def test_token_is_one_time_auth(self):
        '''test: token works only one time'''
        email = 'one-time-test@a.bc'
        token = Token.objects.create(email=email)
        user = TokenAuthenticationBackend().authenticate(uid=token.uid)
        user = TokenAuthenticationBackend().authenticate(uid=token.uid)
        self.assertIsNone(user)

class DjangoAuthenticationTest(TestCase):
    '''testing django calls to authentication backend'''


    @patch('accounts.authentication.TokenAuthenticationBackend.authenticate')
    def test_django_calls_authentication_method(self, mock_auth):
        '''test: accounts.authentication is called by django'''
        auth.authenticate(uid='django-auth-token')
        self.assertTrue(mock_auth.called)

    @patch('accounts.authentication.TokenAuthenticationBackend.authenticate')
    def test_django_calls_authentication_method_with_kwargs(self, mock_auth):
        '''test: accounts.authentication is called by django'''
        auth.authenticate(uid='kwargs-django-auth-token')
        self.assertTrue(mock_auth.called)

    def test_returns_None_if_no_such_token(self):
        '''test: auth of bad token returns None'''
        result = auth.authenticate(uid='django-no-such-token')
        self.assertIsNone(result)

    def test_returns_new_user_with_correct_email_if_token_exists(self):
        '''test: auth of correct token returns new user with correct email'''
        email = 'django-token-test@a.bc'
        token = Token.objects.create(email=email)
        user = auth.authenticate(uid=token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)

    def test_returns_new_user_with_correct_email_if_token_exists_kwargs(self):
        '''test: django calls auth method with kwargs'''
        email = 'django-kwargs-test@a.bc'
        token = Token.objects.create(email=email)
        user = auth.authenticate(uid=token.uid)
        new_user = User.objects.get(email=email)
        self.assertEqual(user, new_user)
