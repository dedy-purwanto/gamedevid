from django import forms
from .models import Avatar

class AvatarForm(forms.ModelForm):
    def remove_past_avatars(self, user):
        avatars = Avatar.objects.filter(user = user)
        for a in avatars:
            a.delete()
    def save(self, *args, **kwargs):
        user = kwargs.pop('user')
        self.remove_past_avatars(user)
        avatar = super(AvatarForm, self).save(commit = False)
        avatar.user = user
        avatar.save()
        return avatar
    class Meta:
        model = Avatar
        fields = ('image',)
