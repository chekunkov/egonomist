# -*- coding: utf-8 -*-
import cv2
import numpy
import os

faces_dir = '/vagrant/dev/faces'


def train_and_compute_score(selected_images):
    #selected_images = [
    #    '49a8ea18fa1311e28d6322000ae811f0_7.jpg_face_229_89_385_245',
    #    '97456ebcd01b11e28c8022000ae912e8_7.jpg_face_9_333_125_449',
    #    '9d7fdb82165711e38cc022000ae80ec6_7.jpg_face_219_56_370_207'
    #]

    #test_image_name = '49a8ea18fa1311e28d6322000ae811f0_7.jpg_face_229_89_385_245'
    #test_image_name = '9d7fdb82165711e38cc022000ae80ec6_7.jpg_face_219_56_370_207'

    train_images = []
    for image_name in selected_images:
        image_path = os.path.join(faces_dir, image_name)
        im = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)
        im = numpy.asarray(im, dtype=numpy.uint8)
        train_images.append(im)

    model = cv2.createEigenFaceRecognizer()
    model.train(
        numpy.asarray(train_images),
        numpy.asarray([0] * len(train_images))
    )

    files = [
        filename for filename in os.listdir(faces_dir)
        if os.path.isfile(os.path.join(faces_dir, filename))
    ]
    print len(files)
    confidences = []
    for file in files:
        im = cv2.imread(file, cv2.IMREAD_GRAYSCALE)
        im = numpy.asarray(im, dtype=numpy.uint8)
        _, confidence = model.predict(numpy.asarray(im))
        confidences.append(confidence)

    face_score = float(sum(confidences))/len(confidences)
    return len(files), face_score

if __name__ == '__main__':
    selected_images = [
        '49a8ea18fa1311e28d6322000ae811f0_7.jpg_face_229_89_385_245',
        '97456ebcd01b11e28c8022000ae912e8_7.jpg_face_9_333_125_449',
        '9d7fdb82165711e38cc022000ae80ec6_7.jpg_face_219_56_370_207'
    ]
    print train_and_compute_score(selected_images)
