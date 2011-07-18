from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from mptt import forms as mptt_forms
from .models import Tag, TagPost

class TagForm(forms.Form):
    def __init__(self, *args, **kwargs):
        self.post = None
        tag_sticky_initial = None
        tag_optional_initial = None
        if 'post' in kwargs:
            self.post = kwargs.pop('post')
            
            if self.post.sticky_tags:
                tag_sticky_initial = Tag.objects.get(name = self.post.sticky_tags[0])
            else:
                tag_sticky_initial = ""

            tag_optional = self.post.optional_tags
            if tag_optional is not None:
                tag_optional_names = [t.name for t in tag_optional]
                tag_optional_initial = ", ".join(tag_optional_names)

        super(TagForm, self).__init__(*args, **kwargs)
        
        #self.fields['tag_sticky'] = forms.CharField(max_length = 255, initial = tag_sticky_initial)
        self.fields['tag_sticky'] = mptt_forms.TreeNodeChoiceField(queryset=Tag.tree.filter(sticky = True), level_indicator=u'--', initial = tag_sticky_initial)
        self.fields['tag_optional'] = forms.CharField(max_length = 500, required = False, initial = tag_optional_initial)
        self.tags = None
    def clean_tag_sticky(self, *args, **kwargs):
        #Check if tag_sticky exists in our sticky tags, if not, raise an error
        tag_sticky = self.data['tag_sticky']        
        try:
            tag = Tag.objects.get(pk = tag_sticky, sticky = True)
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
                    if len(t) > 30:
                        raise ValidationError("Tag \"%s\" is more than 30 characters maximum" % t)
                    try:
                        tag = Tag.objects.get(name = t)
                        if tag is not None:
                            #If this tag is sticky, raise an error
                            if tag.sticky:
                                raise ValidationError("Tag \"%s\" is sticky, don't put it under optional tags!" % t)
                    except Tag.DoesNotExist:
                        pass
                    tags.append(t)
        if tags is not None:
            self.tags = tags
    def save(self):
        if self.post is None:
            return False
        #Clean up all tags that is related to this posts
        tag_post = TagPost.objects.filter(post = self.post)
        for tp in tag_post:
            tp.delete()

        #Save this the tag and the post to TagPost
        tag_sticky = Tag.objects.get(pk = self.data['tag_sticky']).name
        self.tags = [tag_sticky] + self.tags
        #Remove duplicates from tag list
        self.tags = list(set(self.tags))
        if self.tags is not None:
            if len(self.tags) > 0:
                for t in self.tags:
                    try:
                        tag = Tag.objects.get(name = t)
                    except Tag.DoesNotExist:
                        tag = Tag(name = t, sticky = False)
                        tag.save()
                    tag_post = TagPost(tag = tag, post = self.post)
                    tag_post.save()
        
        return True
