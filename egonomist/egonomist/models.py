from django.conf import settings
from django.db import models
from django.contrib.auth.models import User


class Photo(models.Model):
    user = models.ForeignKey(User, related_name='photos')
    instagram_id = models.CharField(max_length=32)
    image = models.ImageField(upload_to=settings.PHOTOS_ROOT)

    def __unicode__(self):
        return self.instagram_id

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Photo, self).delete(*args, **kwargs)


class Face(models.Model):
    user = models.ForeignKey(User, related_name='faces')
    photo = models.ForeignKey(Photo, related_name='faces')
    image = models.ImageField(upload_to=settings.FACES_ROOT)

    def __unicode__(self):
        return self.image.path

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Face, self).delete(*args, **kwargs)
