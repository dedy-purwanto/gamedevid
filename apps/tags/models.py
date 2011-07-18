from django.db import models
from django.contrib.auth.models import User
from django.template import defaultfilters
from mptt.models import MPTTModel, TreeForeignKey
from posts.models import Post

class Tag(MPTTModel):
    name = models.TextField()
    description = models.TextField(blank = True, null = True)
    sticky = models.BooleanField()
    date_created = models.DateTimeField(auto_now_add = True)
    parent = TreeForeignKey('self', null = True, blank= True, related_name='children')
    def __unicode__(self):
        return self.name
    @property
    def slug(self):
        return defaultfilters.slugify(self.name)
    #Ensure the uniqueness manually, since I can't mange to migrate in production server
    #by using unique attribute
    def save(self, *args, **kwargs):
        if not self.pk:
            tags = Tag.objects.filter(name = self.name)
            if tags.count() > 0:
                return False
        super(Tag, self).save(*args, **kwargs)
    class MPTTMeta:
        level_attr = 'mptt_level'
        order_insertion_by=['name']
    class Meta:
        db_table = u'tag'
class TagPost(models.Model):
    tag = models.ForeignKey(Tag, related_name = 'tagpost')
    post = models.ForeignKey(Post, related_name = 'tags')
    def __unicode__(self):
        return self.tag.name
    class Meta:
        db_table = u'tag_post'
