from django.db import models
from django.contrib.auth.models import User

from posts.models import Post

class Tag(models.Model):
    name = models.TextField()
    description = models.TextField(blank = True, null = True)
    sticky = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add = True)
    def __unicode__(self):
        return self.name
    #Ensure the uniqueness manually, since I can't mange to migrate in production server
    #by using unique attribute
    def save(self, *args, **kwargs):
        if not self.pk:
            tags = Tag.objects.filter(name = self.name)
            if tags.count() > 0:
                return False
        super(Tag, self).save(*args, **kwargs)
    class Meta:
        db_table = u'tag'
class TagPost(models.Model):
    tag = models.ForeignKey(Tag, related_name = 'tagpost')
    post = models.ForeignKey(Post, related_name = 'tags')
    def __unicode__(self):
        return self.tag.name
    class Meta:
        db_table = u'tag_post'
