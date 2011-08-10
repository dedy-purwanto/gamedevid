from django.contrib import admin
from django import forms
from .models import Announcement
from posts.models import Post
class AnnouncementForm(forms.ModelForm):
    post = forms.ModelChoiceField(
        queryset = Post.objects.exclude(title = '').filter(announcement = None).order_by('-id')
    )
    class Meta:
        model = Announcement
class AnnouncementAdmin(admin.ModelAdmin):
    form = AnnouncementForm
admin.site.register(Announcement, AnnouncementAdmin)
