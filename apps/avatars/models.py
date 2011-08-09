from django.db import models
from django.contrib.auth.models import User

class Avatar(models.Model):
    image = models.ImageField(blank= False, null = False, upload_to = 'uploaded_avatars')
    user = models.OneToOneField(User, null = False, blank = False, related_name = 'avatar')
