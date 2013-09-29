# -*- coding: utf-8 -*-
from celery import task
from django.contrib.auth.models import User

from .models import Face
from face_detection import detect_faces, make_face_images
from face_recognition import train_and_compute_score


@task(ignore_results=True)
def detect_faces_for_user(username):
    user = User.objects.get(username=username)
    for photo in user.photos.all():
        image_path = photo.image.path
        valid_faces = detect_faces(image_path)
        for face in valid_faces:
            face_image_path = make_face_images(image_path, face)
            Face.objects.get_or_create(
                user=user,
                photo=photo,
                image=face_image_path
            )


@task(ignore_results=True)
def compute_rank(username, selected_faces_images):
    user = User.objects.get(username=username)
    faces = user.faces.all()
    all_faces_images = [face.image.path for face in faces]
    face_score = train_and_compute_score(
        all_faces_images,
        selected_faces_images
    )
    print face_score
