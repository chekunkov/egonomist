from django.db import models
from django.contrib.auth.models import User


class Photo(models.Model):
    # user = models.ForeignKey(User, related_name='photos')
    instagram_id = models.CharField(max_length=32)
    image = models.ImageField(upload_to='photos')
