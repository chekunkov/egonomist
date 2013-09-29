#!/usr/bin/python
# -*- coding: utf-8 -*-

# Face Detection using OpenCV. Based on sample code from:
# http://python.pastebin.com/m76db1d6b

import sys
import os
import cv

from django.conf import settings


common_dir = '/vagrant/dev'
content_dir = common_dir + '/content'
result_dir = common_dir + '/content_result'
faces_dir = common_dir + '/faces'
haarcascades_dir = '/usr/local/share/OpenCV/haarcascades/'


class Item(object):

    def __init__(self, coordinates):

        if not isinstance(coordinates, tuple):
            raise TypeError("Coordinates should be tuple")
        if len(coordinates) != 4:
            raise ValueError("Coordinates should 4 elements")

        self.x, self.y, self.h, self.w = coordinates
        self.x1 = self.x
        self.y1 = self.y
        self.x2 = self.x + self.h
        self.y2 = self.y + self.w

    def __contains__(self, item):
        if not isinstance(item, Item):
            raise TypeError("Cannot compare Item to {}".format(type(item)))
        if (item.x1 >= self.x1 and item.y1 >= self.y1 and
                    item.x2 <= self.x2 and item.y2 <= self.y2):
            return True
        return False

    def paint_rectangle(self, image):
        cv.Rectangle(
            image,
            (self.x1, self.y1),
            (self.x2, self.y2),
            255
        )


class EyePairs(Item):
    pass


class Face(Item):
    u""""""
    def __init__(self, *args):
        super(Face, self).__init__(*args)
        self.eyepair = None

    def is_valid(self, eyepairs_list):
        """Check if face is valid"""
        inner_eyepairs = [ep for ep in eyepairs_list if ep in self]
        if len(inner_eyepairs) == 1:
            self.eyepair = inner_eyepairs[0]
            return True
        return False


def detect_faces(image_path):
    """Converts an image to grayscale and prints the locations of any
       faces found"""
    # grayscale = cv.CreateImage((image.width, image.height), 8, 1)
    # cv.CvtColor(image, grayscale, cv.CV_BGR2GRAY)

    image = cv.LoadImage(image_path, 0)
    storage = cv.CreateMemStorage # 0)
    # cv.ClearMemStorage(storage)
    # cv.EqualizeHist(grayscale, grayscale)
    cascade = cv.Load(os.path.join(
        haarcascades_dir,
        'haarcascade_frontalface_default.xml'
    ))
    faces = cv.HaarDetectObjects(
        image,
        cascade,
        storage(),
        scale_factor=1.1,
        min_neighbors=2,
        flags=0,  # cv.CV_HAAR_DO_CANNY_PRUNING,
        min_size=(75, 75)
    )
    faces = [Face(coordinates) for coordinates, n in faces]

    eyepair_big_cascade = cv.Load(os.path.join(
        haarcascades_dir,
        'haarcascade_mcs_eyepair_big.xml'
    ))
    eyepairs = cv.HaarDetectObjects(
        image,
        eyepair_big_cascade,
        storage(),
        #1.1,
        #2,
        #cv.CV_HAAR_DO_CANNY_PRUNING,
        #(75, 75)
    )
    eyepairs = [EyePairs(coordinates) for coordinates, n in eyepairs]

    valid_faces = []
    for face in faces:
        face.paint_rectangle(image)
        if not face.is_valid(eyepairs):
            continue
        valid_faces.append(face)
        face.paint_rectangle(image)
        face.eyepair.paint_rectangle(image)
    #for eyepair in eyepairs:
    #    eyepair.paint_rectangle(image)
    return valid_faces


def make_face_images(image_path, face):
    image = cv.LoadImage(image_path)
    new_image = cv.CreateImage((150, 150), image.depth, image.channels)
    image = image[face.y1:face.y2, face.x1:face.x2]
    image_path, dot, ext = image_path.rpartition('.')
    image_name = image_path.rsplit('/')[-1]
    face_image_name = u'{}_face_{}.{}'.format(
        image_name,
        '_'.join(map(str, [face.x1, face.y1, face.x2, face.y2])),
        ext
    )
    face_image_path = os.path.join(settings.FACES_ROOT, face_image_name)
    print face_image_path
    cv.Resize(image, new_image, interpolation=cv.CV_INTER_CUBIC)
    cv.SaveImage(face_image_path, new_image)
    return face_image_path


if __name__ == "__main__":
    if not os.path.exists(result_dir):
        os.mkdir(result_dir)
    image_name = sys.argv[1].split('/')[-1]
    print image_name
    valid_faces = detect_faces(image_name)
    for face in valid_faces:
        face_image_name = make_face_images(image_name, face)
        print face_image_name
