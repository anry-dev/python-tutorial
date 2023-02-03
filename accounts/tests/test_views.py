from django.test import TestCase
from django.urls import reverse
from unittest import skip
from unittest.mock import Mock, patch, call
import accounts.views
from accounts.models import Token

class SendLoginEmailViewTest(TestCase):
    '''testing sending email view'''

    url_name = 'send_login_email'
    url = reverse(url_name)

    @skip('too old, replaced by the next test')
    def test_redirect_to_home_page(self):
        '''test: POST redirected to home page'''
        response = self.client.post(
                self.url,
                data = {'email': 'a@b.c'}
        )
        self.assertRedirects(response, '/')

    def test_sends_mail_to_address_from_post(self):
        '''test: sending email from post request'''
        self.send_mail_called = False

        def fake_send_mail(subject, body, from_email, to_list):
            '''fake send_mail function'''
            self.send_mail_called = True
            self.subject = subject
            self.body = body
            self.from_email = from_email
            self.to_list = to_list
            
        accounts.views.send_mail = fake_send_mail

        response = self.client.post(
                self.url,
                data = {'email': 'a@b.c'}
        )
        
        self.assertRedirects(response, '/')
        self.assertTrue(self.send_mail_called)
        self.assertEqual(self.subject, 'Your login link for Superlists')
        self.assertEqual(self.from_email, 'superlist@lab.rt.ru')
        self.assertEqual(self.to_list, ['a@b.c'])


    def test_sends_mail_to_address_from_post_mock_version(self):
        '''test: sending email from post request - using mock'''

        m = Mock()
        m.send_mail.return_value = True
        accounts.views.send_mail = m.send_mail

        response = self.client.post(
                self.url,
                data = {'email': 'a@b.c'}
        )

        args = m.send_mail.call_args[0]

        self.assertRedirects(response, '/')
        self.assertTrue(m.send_mail.called)
        self.assertEqual(args[0], 'Your login link for Superlists')
        self.assertEqual(args[2], 'superlist@lab.rt.ru')
        self.assertEqual(args[3], ['a@b.c'])

    @patch('accounts.views.send_mail')
    def test_sends_mail_to_address_from_post_patch_version(self, mock_send_mail):
        '''test: sending email from post request - using mock'''

        response = self.client.post(
                self.url,
                data = {'email': 'a@b.c'}
        )

        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args

        self.assertRedirects(response, '/')
        self.assertTrue(mock_send_mail.called)
        self.assertEqual(subject, 'Your login link for Superlists')
        self.assertEqual(from_email, 'superlist@lab.rt.ru')
        self.assertEqual(to_list, ['a@b.c'])

    def test_send_mail_returns_success_message(self):
        '''test: got success message after sending mail'''
        response = self.client.post(
                self.url,
                data = {'email': 'a@b.c'},
                follow = True
        )

        message = list(response.context['messages'])[0]
        self.assertEqual(
                message.message,
                'Check your mail'
        )

    @patch('accounts.views.messages')
    def test_send_mail_returns_success_message_with_patch(self, mock_messages):
        '''test: got success message after sending mail'''
        response = self.client.post(
                self.url,
                data = {'email': 'a@b.c'}
        )

        expected_msg = 'Check your mail'
        self.assertEqual(
                mock_messages.success.call_args,
                call(response.wsgi_request, expected_msg),
        )

    def test_creates_token_assosiated_with_email(self):
        '''test: created token assosiated with email'''
        self.client.post(
                self.url,
                data = {'email': 'a@b.c'}
        )
        token = Token.objects.first()
        self.assertEqual(token.email, 'a@b.c')

    @patch('accounts.views.send_mail')
    def test_returns_token_assosiated_with_email_by_mail(self, mock_send_mail):
        '''test: token assosiated with email is sent by mail'''
        self.client.post(
                self.url,
                data = {'email': 'a@b.c'}
        )
        token = Token.objects.first()
        expected_url = f'http://testserver/accounts/login?token={token.uid}'
        (subject, body, from_email, to_list), kwargs = mock_send_mail.call_args
        self.assertIn(expected_url, body)

@patch('accounts.views.auth')
class LoginViewTest(TestCase):
    '''testing login view'''

    url_name = 'accounts_login'
    url = reverse(url_name)

    def test_login_page_redirects_to_home_page(self, mock_auth):
        '''test: request to login page is redirected to home page'''
        #print(reverse('accounts_login')) #, args=('/login?token=abcd123',)))
        response = self.client.get(f'{self.url}?token=abcd123')
        self.assertRedirects(response, '/')

    def test_login_page_calls_authenticate_with_uid_from_request(self, mock_auth):
        '''test: login page calls auth method with uid from request'''
        uid = 'auth-test-uid'
        response = self.client.get(f'{self.url}?token={uid}')
        self.assertEqual(
            mock_auth.authenticate.call_args,
            call(uid=uid)
        )

    def test_login_page_login_user_if_exists(self, mock_auth):
        '''test: login page login user it exists'''
        uid = 'auth-test-uid'
        response = self.client.get(f'{self.url}?token={uid}')
        self.assertEqual(
            mock_auth.login.call_args,
            call(response.wsgi_request, mock_auth.authenticate.return_value)
        )

    def test_does_not_login_if_authentication_fails(self, mock_auth):
        '''test: do not call login if user does not exist'''
        uid = 'auth-test-uid'
        mock_auth.authenticate.return_value = None
        response = self.client.get(f'{self.url}?token={uid}')
        self.assertFalse(mock_auth.login.called)

