from django.db import models
from posts.models import Post

class Announcement(models.Model):   
    post = models.OneToOneField(Post, null = False, related_name = 'announcement')
    def __unicode__(self):
        return self.post.title
