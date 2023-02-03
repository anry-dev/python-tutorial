from django.test import TestCase
from django.contrib import auth
from django.core.exceptions import ValidationError
from accounts.models import Token

User = auth.get_user_model()

class UserModelTest(TestCase):
    '''test user model'''

    def test_user_is_valid_with_email_only(self):
        '''test: user is valid if email exists'''
        user = User(email='a@b.com')
        user.full_clean()   # must not through an exception

    def test_email_is_primary_key(self):
        '''test: email field is the primary key'''
        user = User(email='a@b.c')
        self.assertEqual(user.pk, 'a@b.c')

    def test_user_login_works(self):
        '''test: valid users can auth.login'''
        user = User.objects.create(email='login-test@a.b')
        #user.backend = ''
        request = self.client.request().wsgi_request
        auth.login(request, user)

class TokenModelTest(TestCase):
    '''test token model'''

    def test_links_user_with_auth_generated_uid(self):
        '''test: two tokens for the same user are different'''
        token1 = Token.objects.create(email='a@b.c')
        token2 = Token.objects.create(email='a@b.c')
        self.assertNotEqual(token1.uid, token2.uid)
