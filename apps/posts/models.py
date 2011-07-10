from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.TextField(blank = True, null = True)
    content = models.TextField(blank = False, null = False)
    author = models.ForeignKey(User, related_name = "post")
    date_created = models.DateTimeField(auto_now_add = True)
    parent = models.ForeignKey("self", related_name = "post_parent", blank = True, null = True)
    def __unicode__(self):
        return self.title
    @staticmethod
    def get_latests():
        return Post.objects.filter(parent = None).order_by('-id')
    def get_replies(self):
        return Post.objects.filter(parent = self).order_by('id')
    def get_last_reply(self):
        return self.get_replies().all().latest('id')
    class Meta:
        db_table = u'post'
