from django import forms
from django.forms import ValidationError
from datetime import datetime 
from django.contrib.auth.models import User
from tinymce.widgets import TinyMCE
from models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField(required = True)
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        parent = None
        quick_reply = False
        if 'parent' in kwargs:
            parent = kwargs.pop('parent')
        if 'quick_reply' in kwargs:
            quick_reply = kwargs.pop('quick_reply')

        super(PostForm, self).__init__(*args, **kwargs)
        
        is_reply = False
        if self.instance.pk:
            if self.instance.parent:
                is_reply = True
        if parent: #If it's in reply mode, don't use title
            is_reply = True
            self.instance.parent = parent
        
        if is_reply:
            self.fields.pop('title')

        content_cols = 80
        content_rows = 20
        if quick_reply:
            content_cols = 50
            content_rows = 10
        
        self.fields['content'] = forms.CharField(widget=TinyMCE(attrs={'cols':content_cols, 'rows':content_rows}))
    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            if self.instance.pk:
                return title
        except:
            pass
        
        if len(title) < 20:
            raise ValidationError("Your title is too short!")

        try:
            post = Post.objects.get(title = title)
            if post is not None:
                raise ValidationError("This title already exists")
        except Post.DoesNotExist:
            return title
    def clean_content(self):
        content = self.cleaned_data['content']
        try:
            if self.instance.pk:
                return content
        except:
            pass

        if len(content) < 30:
            raise ValidationError("Your post is too short!")

        try:
            post = Post.objects.get(content = content)
            if post is not None:
                raise ValidationError("This content already exists")
        except Post.DoesNotExist:
            return content
    def is_valid(self):
        is_valid = super(PostForm, self).is_valid()
        try:
            if self.instance:
                if is_valid:
                    if self.instance.author == self.author or self.author.is_superuser or self.author.is_staff:
                        return True
                    else:
                        return False
        except:
            pass
        return is_valid
    def save(self):
        if not self.instance.pk: #it's a new post/reply
            self.instance.author = self.author
            if self.instance.parent is None:
                self.instance.date_sorted = datetime.now()
            else:
                self.instance.parent.date_sorted = datetime.now()
                self.instance.parent.save()
        return super(PostForm, self).save(commit = True)
        
    class Meta:
        model = Post
        exclude = ('author','parent')
