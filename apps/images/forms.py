from django import forms
from .models import Image

class ImageForm(forms.ModelForm):
    def save(self, *args, **kwargs):
        post = kwargs.pop('post')
        image = super(ImageForm, self).save(commit = False)
        image.post = post
        image.save()
        return image
    class Meta:
        model = Image
        fields = ('image',)
