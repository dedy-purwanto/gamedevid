from django.db import models
from django.contrib.auth.models import User
from images.models import Image

class Genre(models.Model):
    genre = models.CharField(max_length = 255)
    def __unicode__(self):
        return self.genre

class Platform(models.Model):
    platform = models.CharField(max_length = 255)
    def __unicode__(self):
        return self.platform

class Game(Image):
    download_url = models.URLField(blank = True)
    developer = models.CharField(blank = True, max_length = 255)
    release_date = models.CharField(blank = True, max_length = 255)
    genre = models.ManyToManyField(Genre)
    platform = models.ManyToManyField(Platform)


