
from django.contrib.auth.models import User

class TestUtils():
    @staticmethod
    def generate_users():
        users = (
                 ('admin', 'admin@localhost','123',True),
                 ('kecebongsoft', 'kecebongsoft@localhost','123',False),
                 ('dedi', 'dedi@localhost','123',False),
                )
        for u in users:
            user = User.objects.create_user(username = u[0], email = u[1], password = u[2])
            user.is_staff = u[3]
            user.save()
        return True
