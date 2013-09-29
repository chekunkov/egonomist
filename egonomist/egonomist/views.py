from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile

import requests
from instagram import InstagramAPI

from .models import Photo, Face


api = InstagramAPI(
    client_id=settings.INSTAGRAM_CLIENT_ID,
    client_secret=settings.INSTAGRAM_CLIENT_SECRET,
    redirect_uri=settings.LOGIN_REDIRECT_URL
)


def hello(request):
    url = api.get_authorize_login_url(scope=settings.INSTAGRAM_SCOPE)
    return render(request, 'dindex.html', {'url': url})


def complete(request):
    code = request.GET['code']
    access_token = api.exchange_code_for_access_token(code)
    auth_api = InstagramAPI(access_token=access_token[0])
    user, _ = User.objects.get_or_create(
        username=access_token[1].get('username')
    )

    # Move to worker
    recent_media, _ = auth_api.user_recent_media(count=-1)
    for media in recent_media:
        photo, created = Photo.objects.get_or_create(
            user=user,
            instagram_id=media.id
        )
        if created:
            img_temp = NamedTemporaryFile(delete=True)
            with img_temp:
                request = requests.get(media.images['standard_resolution'].url, stream=True)
                for block in request.iter_content(1024):
                    if not block:
                        break
                    img_temp.write(block)
                img_temp.flush()

                photo.image.save('{}.jpg'.format(photo.instagram_id), File(img_temp))

    return redirect('choose')


def choose(request):
    faces = Face.objects.filter(user=request.user)[:8]
    return render(request, 'dchoose.html', {'faces':[faces[:4], faces[4:]]})
