from django.db import models
import md5
class User(models.Model):
    id = models.IntegerField(primary_key=True)
    username = models.CharField(max_length=100)
    password = models.CharField(max_length=32)
    salt =  models.CharField(max_length=3)
    
    @staticmethod
    def authenticate(username, password):
        user = None
        try:
            user = User.objects.get(username = username)
            if user:
                password = md5.new(password).hexdigest()
                password = md5.new(password + user.salt).hexdigest()
                if password == user.password:
                    return user
                else:
                    return None
        except User.DoesNotExist:
            return None

        return user

    class Meta:
        db_table = 'old_user'
