from django.shortcuts import render, redirect
from django.conf import settings
from django.contrib.auth.models import User
from django.core.files import File
from django.core.files.temp import NamedTemporaryFile
from django.http import HttpResponse, HttpResponseRedirect

from django.contrib.auth import login, authenticate

import requests
from instagram import InstagramAPI
from face_detection import make_face_images, detect_faces
from face_recognition import train_and_compute_score

from .models import Photo, Face
import json


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
    # Don't repeat this!
    user.backend = 'django.contrib.auth.backends.ModelBackend'
    #authenticate(username=user.username, password=user.password)
    login(request, user)

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

    for face in Face.objects.filter(user=user):
        face.delete()

    for photo in user.photos.all():
        image_path = photo.image.path
        valid_faces = detect_faces(image_path)
        for face in valid_faces:
            face_image_path = make_face_images(image_path, face)
            with open(face_image_path) as f:
                Face.objects.get_or_create(
                    user=user,
                    photo=photo,
                    image=File(f)
                )
    return redirect('choose')


def choose(request):
    faces = Face.objects.filter(user=request.user)[:8]
    #import ipdb; ipdb.set_trace()
    len_faces = len(faces)
    if len_faces < 8:
        return HttpResponseRedirect('/result?result={}'.format(len_faces))
    return render(request, 'dchoose.html', {
        'faces': [
            faces[:4],
            faces[4:]
        ]
    })


def compute_result(request):
    ids = request.GET.getlist('ids[]')
    user = request.user

    selected_faces = Face.objects.filter(user=user, id__in=ids)
    selected_images = [face.image.path for face in selected_faces]
    all_images = [
        face.image.path for face
        in Face.objects.filter(user=user)
    ]
    result = train_and_compute_score(all_images, selected_images)
    result = round(100 * float(result) / len(all_images))
    return HttpResponse(json.dumps(result), content_type='application/json')


def result(request):
    result = request.GET['result']
    return render(request, 'dresult.html', {
        'result': int(result)
    })
