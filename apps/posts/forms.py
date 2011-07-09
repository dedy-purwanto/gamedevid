from django.forms import ModelForm
from django.forms import ValidationError

from django.contrib.auth.models import User
from models import Post

class PostForm(ModelForm):

    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(PostForm, self).__init__(*args, **kwargs)
    def save(self):
        post = super(PostForm, self).save(commit = False)
        post.author = self.author
        post.save()
    class Meta:
        model = Post
        exclude = ('author',)
