from django.core.urlresolvers import reverse
from django.contrib.auth.models import User
from django.test import TestCase
from django.test import Client

from .forms import LoginForm, RegisterForm

class TestUtils():
    @staticmethod
    def generate_users():
        users = (
                 ('admin', 'admin@localhost.com','123',True),
                 ('kecebongsoft', 'kecebongsoft@localhost.com','123',False),
                 ('dedi', 'dedi@localhost.com','123',False),
                )
        for u in users:
            user = User.objects.create_user(username = u[0], email = u[1], password = u[2])
            user.is_staff = u[3]
            user.save()
        return True

#Test login via object
class LoginFormTest(TestCase):
    def setUp(self):
        TestUtils.generate_users()
    def test_invalid_username(self):
        form = LoginForm({'username' : 'invalid_username', 'password' : '123'})
        self.assertFalse(form.is_valid())
    def test_invalid_password(self):
        form = LoginForm({'username' : 'kecebongsoft', 'password' : 'invalid_password'})
        self.assertFalse(form.is_valid())
    def test_username_password(self):
        form = LoginForm({'username' : 'kecebongsoft', 'password' : '123'})
        self.assertTrue(form.is_valid())
#Test login via view
class LoginTest(TestCase):
    def setUp(self):
        TestUtils.generate_users()
    def test_login(self):
        response = self.client.post(
                reverse('users:login'),
                {
                    'username' : 'kecebongsoft',
                    'password' : '123',
                }
            )
        #Must redirect to somewhere upon succesful login
        self.assertEqual(response.status_code, 302)

#Test register via object
class RegisterFormTest(TestCase):
    def setUp(self):
        TestUtils.generate_users()
    def test_no_username(self):
        form = RegisterForm({'username' : '',
                             'email' : 'new_user@localhost.com',
                             'password' : '123',
                             'confirm_password' : '123'
                            })
        self.assertFalse(form.is_valid())
    def test_no_email(self):
        form = RegisterForm({'username' : 'new_user',
                             'email' : '',
                             'password' : '123',
                             'confirm_password' : '123'
                            })
        self.assertFalse(form.is_valid())
    def test_no_password(self):
        form = RegisterForm({'username' : 'new_user',
                             'email' : 'new_user@localhost.com',
                             'password' : '',
                             'confirm_password' : '123'
                            })
        self.assertFalse(form.is_valid())
    def test_no_confirm_password(self):
        form = RegisterForm({'username' : 'new_user',
                             'email' : 'new_user@localhost.com',
                             'password' : '123',
                             'confirm_password' : ''
                            })
        self.assertFalse(form.is_valid())
    def test_invalid_email(self):
        form = RegisterForm({'username' : 'new_user',
                             'email' : 'new_user_invalid_email',
                             'password' : '123',
                             'confirm_password' : '123'
                            })
        self.assertFalse(form.is_valid())
    def test_password_mismatch(self):
        form = RegisterForm({'username' : 'new_user',
                             'email' : 'new_user@localhost.com',
                             'password' : '123',
                             'confirm_password' : '456'
                            })
        self.assertFalse(form.is_valid())
    def test_username_exists(self):
        user = User.objects.get(username = 'kecebongsoft')
        form = RegisterForm({'username' : 'kecebongsoft',
                             'email' : 'new_user@localhost.com',
                             'password' : '123',
                             'confirm_password' : '123'
                            })
        self.assertFalse(form.is_valid())
    def test_valid(self):
        form = RegisterForm({'username' : 'new_user',
                             'email' : 'new_user@localhost.com',
                             'password' : '123',
                             'confirm_password' : '123'
                            })
        self.assertTrue(form.is_valid())
#Test register via view
class RegisterTest(TestCase):
    def setUp(self):
        TestUtils.generate_users()
    def test_register(self):
        response = self.client.post(
                reverse('users:register'),
                {
                    'username' : 'new_user',
                    'email' : 'new_user@localhost.com',
                    'password' : '123',
                    'confirm_password' : '123'
                }
            )
        #Must redirect to somewhere upon succesful registration
        self.assertEqual(response.status_code, 302)
