from django.db import models
from django.contrib.auth.models import User

class PhotoQuerySet(models.query.QuerySet):
    def delete(self):
        for photo in self:
            photo.image.delete()


class PhotoManager(models.Manager):
    def get_query_set(self):
        return PhotoQuerySet(self.model)

class Photo(models.Model):
    user = models.ForeignKey(User, related_name='photos')
    instagram_id = models.CharField(max_length=32)
    image = models.ImageField(upload_to='photos')

    objects = PhotoManager()

    def __unicode__(self):
        return self.instagram_id

    def delete(self, *args, **kwargs):
        self.image.delete()
        super(Photo, self).delete(*args, **kwargs)
