from django import forms
from django.forms import ValidationError
from django.contrib.auth.models import User
from models import Post

class PostForm(forms.ModelForm):
    title = forms.CharField()
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(PostForm, self).__init__(*args, **kwargs)
    def clean_title(self):
        title = self.cleaned_data['title']
        try:
            if self.instance.pk:
                return title
        except:
            pass
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
        post = super(PostForm, self).save(commit = False)
        if not self.instance.pk:
            post.author = self.author
        post.save()
        return post
    class Meta:
        model = Post
        exclude = ('author','parent')
