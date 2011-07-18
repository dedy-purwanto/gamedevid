from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters

# Create your models here.
class Post(models.Model):
    title = models.TextField(blank = True, null = True)
    content = models.TextField(blank = False, null = False)
    author = models.ForeignKey(User, related_name = "post")
    date_created = models.DateTimeField(auto_now_add = True)
    parent = models.ForeignKey("self", related_name = "post_parent", blank = True, null = True)
    date_sorted = models.DateTimeField(blank = True, null = True) #Filled only for parent thread, for sorting purpose (need improvement later)
    def __unicode__(self):
        return self.title
    @property
    def sticky_tags(self):
        return self.tags.filter(tag__sticky = True)
    @property
    def optional_tags(self):
        tags = []
        for t in self.tags.all().order_by('-id'):
            if not t.tag.sticky:
                tags.append(t.tag)
        return tags if len(tags) > 0 else None
    @staticmethod
    def get_latests():
        return Post.objects.filter(parent = None).order_by('-date_sorted')
    def get_replies(self):
        return Post.objects.filter(parent = self).order_by('id')
    def get_last_reply(self):
        return self.get_replies().all().order_by('-id').latest('id')
    def title_slug(self):
        return defaultfilters.slugify(self.title)
    class Meta:
        db_table = u'post'
