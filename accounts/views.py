from django.shortcuts import render, redirect
from django.core.mail import send_mail
from django.contrib import messages, auth
from django.urls import reverse
from accounts.models import Token

import logging
logger = logging.getLogger(__name__)
logger.debug(f'views module: {__name__}')

# Create your views here.
def send_login_email(request):
    '''accounts login parser'''
    if request.method == 'POST':
        email = request.POST['email']
        token = Token.objects.create(email=email)
        url = request.build_absolute_uri(
                reverse('accounts_login') + f'?token={token.uid}'
        )
        logger.debug(f'login url: {url}')
        body = f'Use this link to log in:\n\n{url}'
        send_mail(
            'Your login link for Superlists',
            body,
            'superlist@lab.rt.ru',
            [email],
        )

    messages.success(
            request,
            'Check your mail'
    )
    return redirect('/')

def login(request):
    '''make user registration in the system'''
    token = request.GET.get('token')
    user = auth.authenticate(uid=request.GET.get('token'))
    if user is not None:
        auth.login(request, user)

    return redirect('/')
