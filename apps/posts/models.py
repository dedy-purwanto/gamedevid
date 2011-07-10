from django.db import models
from django.contrib.auth.models import User

# Create your models here.
class Post(models.Model):
    title = models.TextField(blank = False, null = False)
    content = models.TextField(blank = False, null = False)
    author = models.ForeignKey(User, related_name = "post")
    date_created = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.title
    @staticmethod
    def get_latests():
        return Post.objects.all().order_by('-id')
    class Meta:
        db_table = u'post'
