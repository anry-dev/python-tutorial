from django.conf import settings
from django.contrib.auth import BACKEND_SESSION_KEY, SESSION_KEY, get_user_model
from django.contrib.sessions.backends.db import SessionStore
from .base import FunctionalTest

User = get_user_model()

class MyListsTest(FunctionalTest):
    '''test users own todo lists'''

    def create_pre_authenticated_session(self, email):
        '''make web sessions authenticated on the server'''
        user = User.objects.create(email=email)
        session = SessionStore()
        session[SESSION_KEY] = user.pk
        session[BACKEND_SESSION_KEY] = settings.AUTHENTICATION_BACKENDS[0]
        session.save()

        # set cookies for the browser
        # page 404 loads faster then other
        self.browser.get(self.live_server_url + '/404_no_such_url/')
        self.browser.add_cookie(dict(
            name=settings.SESSION_COOKIE_NAME,
            value=session.session_key,
            path='/',
        ))

    def test_logged_in_users_lists_are_saved_as_my_lists(self):
        '''test: lists for the authenticated users are saved as my_lists'''
        email = 'registered@a.b.c'
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_out(email)

        # Эдит является зарегистриованным пользователем
        # она подключается к системе и видит свои списки
        self.create_pre_authenticated_session(email)
        self.browser.get(self.live_server_url)
        self.wait_to_be_logged_in(email)