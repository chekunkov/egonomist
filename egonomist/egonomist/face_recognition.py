# -*- coding: utf-8 -*-
import cv2
import numpy
import os


def train_and_compute_score(all_images, selected_images):
    train_images = []
    for image_path in selected_images:
        im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        im = numpy.asarray(im, dtype=numpy.uint8)
        train_images.append(im)

    model = cv2.createEigenFaceRecognizer()
    #model = cv2.createLBPHFaceRecognizer()
    model.train(
        numpy.asarray(train_images),
        numpy.asarray([0] * len(train_images))
    )

    confidences = []
    counter = 0
    for image in all_images:
        #if image in selected_images:
        #    continue
        im = cv2.imread(image, cv2.IMREAD_GRAYSCALE)
        im = numpy.asarray(im, dtype=numpy.uint8)
        _, confidence = model.predict(numpy.asarray(im))
        if confidence < 2000:
            counter += 1
        print _, confidence, image
        confidences.append(confidence)


    #face_score = float(sum(confidences))/len(confidences)
    #from math import sqrt
    #face_score = 1.0 - sqrt(float(face_score) / (len(selected_images) * num_eigens)) / 255.0
    return counter

if __name__ == '__main__':

    faces_dir = '/vagrant/dev/faces'

    all_images = [
        os.path.join(faces_dir, filename)
        for filename in os.listdir(faces_dir)
        if os.path.isfile(os.path.join(faces_dir, filename))
    ]

    selected_images = [
        '49a8ea18fa1311e28d6322000ae811f0_7.jpg_face_229_89_385_245',
        '97456ebcd01b11e28c8022000ae912e8_7.jpg_face_9_333_125_449',
        '9d7fdb82165711e38cc022000ae80ec6_7.jpg_face_219_56_370_207'
    ]
    selected_images = [os.path.join(faces_dir, i) for i in selected_images]
    print train_and_compute_score(sorted(all_images), selected_images)
