from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters

# Create your models here.
class Post(models.Model):
    title = models.TextField(blank = True)
    content = models.TextField(blank = False)
    author = models.ForeignKey(User, related_name = "post")
    date_created = models.DateTimeField(auto_now_add = True)
    parent = models.ForeignKey("self", null = True)
    date_sorted = models.DateTimeField(blank = True, null = True) #Filled only for parent thread, for sorting purpose (need improvement later)
    def __unicode__(self):
        if self.title:
            return self.title
        return u'' #For legacy support since last time we still have null-able titles
        
    @property
    def content_short(self):
        if len(self.content) < 255:
            return self.content
        return self.content[:255] + "..."
    @property
    def title_short(self):
        if len(self.title) < 20:
            return self.title
        return self.title[:20] + "..."
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
    def get_readers(self):
        return [r.user for r in self.reader.all()]
    class Meta:
        db_table = u'post'


"""
Ability to show unread posts to some particular users.

Everytime a new posts/reply has been made, we remove all entry of that post in this table
That simply means, nobody has read it. When a particular user open that post, we added
that user along with the post that he opened, that means that user has read it. When
another user makes a reply in that post, remove entry of that post again.

We only store the parent of the post. that means, reply will not be stored, instead, it's
parent will be stored.
"""

class PostReader(models.Model):
    user = models.ForeignKey(User, related_name = 'reader')
    post = models.ForeignKey(Post, related_name = 'reader')
    date_created = models.DateTimeField(auto_now_add = True)
    @staticmethod
    def clear(post):
        readers = PostReader.objects.filter(post = post)
        for r in readers:
            r.delete()
    @staticmethod
    def add(user, post):
        try:
            reader = PostReader.objects.get(user = user, post = post)
        except PostReader.DoesNotExist:
            reader = PostReader(user = user, post = post)
            reader.save()
        return reader
    class Meta:
        db_table = u'post_reader'
