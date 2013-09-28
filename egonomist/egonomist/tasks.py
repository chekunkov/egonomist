# -*- coding: utf-8 -*-
from celery import task


from face_detection import detect_faces, make_face_images


@task(ignore_results=True)
def detect_face(images_list):
    for image in images_list:
        valid_faces = detect_faces(image)
        for face in valid_faces:
            face_image_name = make_face_images(image, face)
            print face_image_name
