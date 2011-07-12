from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User

from .models import Tag, TagPost

class TagForm(forms.Form):
    tag_sticky = forms.CharField(max_length = 255)
    tag_optional  = forms.CharField(max_length = 500, required = False)
    def __init__(self, *args, **kwargs):
        self.post = kwargs.pop('post')
        self.tags = None
        super(TagForm, self).__init__(*args, **kwargs)
    def clean_tag_sticky(self, *args, **kwargs):
        #Check if tag_sticky exists in our sticky tags, if not, raise an error
        tag_sticky = self.data['tag_sticky']        
        try:
            tag = Tag.objects.get(name = tag_sticky)
        except Tag.DoesNotExist:
            raise ValidationError("Tag %s is not in the sticky tag list masbro" % tag_sticky)
    def clean_tag_optional(self, *args, **kwargs):
        #Check if optional tags exists, if it is, fetch it, if not, create a new one and fetch it
        tags = None
        tag_optional = self.data['tag_optional'] if 'tag_optional' in self.data else None
        if tag_optional is not None:
            tags = []
            tags_optional = tag_optional.split(',')
            for t in tags_optional:
                t = t.strip()
                if len(t) > 0:
                    try:
                        tag = Tag.objects.get(name = t)
                        if tag is not None:
                            #If this tag is sticky, raise an error
                            if tag.sticky:
                                raise ValidationError("Tag %s is sticky, don't put it under optional tags!" % t)
                    except Tag.DoesNotExist:
                        pass
                    tags.append(t)
        if tags is not None:
            self.tags = tags
    def save(self):
        #Clean up all tags that is related to this posts
        tag_post = TagPost.objects.filter(post = self.post)
        for tp in tag_post:
            tp.delete()

        #Save this the tag and the post to TagPost
        if self.tags is not None:
            if len(self.tags) > 0:
                for t in self.tags:
                    try:
                        tag = Tag.objects.get(name = t)
                    except Tag.DoesNotExist:
                        tag = Tag(name = t, sticky = False)
                        tag.save()
                    tag_post = TagPost()
                    tag_post.tag = tag
                    tag_post.post = self.post
                    tag_post.save()
        
        return True
