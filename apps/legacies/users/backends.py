from .models import User as LegacyUser
from django.contrib.auth.models import User
import hashlib
class Authentication:
    def authenticate(self, username = None, password = None):
        #If this user already registered in our main user db, ignore this legacy authentication
        try:
            user = User.objects.get(username = username)
            if user:
                return None
        except User.DoesNotExist:
            pass

        old_user = LegacyUser.authenticate(username, password)
        if old_user:
            try:
                user = User.objects.get(username = username)
            except User.DoesNotExist:
                new_password = 'sha1$%s$%s' % (old_user.salt, hashlib.sha1(old_user.password).hexdigest())
                user = User(username = username, password = new_password)
                
                user.is_staff = False
                user.is_superuser = False
                user.save()
            return user
        return None
    def get_user(self, user_id):
        try:
            return User.objects.get(pk = user_id)
        except User.DoesNotExist:
            return None
