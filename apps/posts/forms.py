from django.forms import ModelForm
from django.forms import ValidationError
from django.contrib.auth.models import User
from models import Post

class PostForm(ModelForm):
    def __init__(self, *args, **kwargs):
        self.author = kwargs.pop('author')
        super(PostForm, self).__init__(*args, **kwargs)
    def clean_title(self):
        title = self.data['title']
        try:
            post = Post.objects.get(title = title)
            if post is not None:
                raise ValidationError("This title already exists")
        except Post.DoesNotExist:
            return title
    def clean_content(self):
        title = self.data['content']
        try:
            post = Post.objects.get(title = title)
            if post is not None:
                raise ValidationError("This content already exists")
        except Post.DoesNotExist:
            return title
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
        post.author = self.author
        post.save()
        return post
    class Meta:
        model = Post
        exclude = ('author',)
