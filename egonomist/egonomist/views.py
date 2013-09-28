# Create your views here.
from django.shortcuts import render
from django.conf import settings

from instagram import InstagramAPI


api = InstagramAPI(
        client_id=settings.INSTAGRAM_CLIENT_ID,
        client_secret=settings.INSTAGRAM_CLIENT_SECRET,
        redirect_uri=settings.LOGIN_REDIRECT_URL)


def hello(request):
    url = api.get_authorize_login_url(scope=settings.INSTAGRAM_SCOPE)
    return render(request, 'index.html', {'url': url})


def complete(request):
    code = request.GET['code']
    access_token = api.exchange_code_for_access_token(code)