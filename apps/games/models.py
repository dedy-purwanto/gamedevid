from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
class Genre(models.Model):
    genre = models.CharField(max_length = 255)
    def __unicode__(self):
        return self.genre

class Platform(models.Model):
    platform = models.CharField(max_length = 255)
    def __unicode__(self):
        return self.platform

class Game(models.Model):
    image = models.ImageField(blank= False, null = False, upload_to = 'uploaded_images')
    post = models.ForeignKey(Post, null = False, blank=False, related_name = 'game')
    download_url = models.URLField(blank = True)
    developer = models.CharField(blank = True, max_length = 255)
    release_date = models.CharField(blank = True, max_length = 255)
    genre = models.ManyToManyField(Genre)
    platform = models.ManyToManyField(Platform)
    @property
    def platform_join(self):
        return ', '.join( [ p.platform for p in self.platform.all() ] )
    @property
    def genre_join(self):
        return ', '.join( [ g.genre for g in self.genre.all() ] )
