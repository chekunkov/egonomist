import os

from django.conf import settings
from django.db import models
from django.contrib.auth.models import User
from django.core.files.storage import FileSystemStorage
from django.conf import settings


class PhotoQuerySet(models.query.QuerySet):
    def delete(self):
        for photo in self:
            photo.image.delete()
        super(self, PhotoQuerySet).delete()


class PhotoManager(models.Manager):
    def get_query_set(self):
        return PhotoQuerySet(self.model)

class Photo(models.Model):
    user = models.ForeignKey(User, related_name='photos')
    instagram_id = models.CharField(max_length=32)
    image = models.ImageField(upload_to=settings.PHOTOS_ROOT)

    objects = PhotoManager()

    def __unicode__(self):
        return self.instagram_id

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Photo, self).delete(*args, **kwargs)


class Face(models.Model):
    user = models.ForeignKey(User, related_name='faces')
    photo = models.ForeignKey(Photo, related_name='faces')
    image = models.ImageField(upload_to='faces')

    def __unicode__(self):
        return self.image.path

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Face, self).delete(*args, **kwargs)

    @property
    def relpath(self):
        return os.path.relpath(self.image.path, settings.MEDIA_ROOT)
