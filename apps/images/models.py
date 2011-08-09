from django.db import models
from django.contrib.auth.models import User
from posts.models import Post
class Image(models.Model):
    image = models.ImageField(blank = False, null = False, upload_to = 'uploaded_images')
    post = models.OneToOneField(Post, null = False, blank=False, related_name = 'image')
