from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.TextField(blank = False, null = False, unique = True)
    content = models.TextField(blank = False, null = False, unique = True)
    author = models.ForeignKey(User, related_name = "post")
    def __unicode__(self):
        return self.title
    class Meta:
        db_table = u'post'
