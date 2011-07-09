from django import forms
from django.contrib import auth
from django.contrib.auth.models import User

class LoginForm(forms.Form):
    username = forms.CharField()
    password = forms.CharField(widget=forms.PasswordInput())
    def clean(self, *args, **kwargs):
        if self.errors:
            return
        username = self.data['username']
        password = self.data['password']
        self.user = auth.authenticate(username=username, password=password)
        if username and password:
            if self.user is not None:
                if not self.user.is_active:
                    raise forms.ValidationError("Inactive user.")
            else:
                raise forms.ValidationError("Bad username or password.")
        return self.data
    def save(self, *args, **kwargs):
        return self.user

class RegisterForm(forms.Form):
    username = forms.CharField(required = True)
    email = forms.EmailField(required = True)
    password = forms.CharField(widget = forms.PasswordInput(), required = True)
    confirm_password = forms.CharField(widget = forms.PasswordInput(), required = True)
    def clean_confirm_password(self):
        password = self.data['password']
        confirm_password = self.data['confirm_password']
        if not password == confirm_password:
            raise forms.ValidationError("Password mismatched")
        return password
    def clean_username(self):
        username = self.data['username']
        try:
            user = User.objects.get(username = username)
            if user is not None:
                raise forms.ValidationError("Username already exists")
        except User.DoesNotExist:
            return username
    def save(self, *args, **kwargs):
        username = self.data['username']
        password = self.data['password']
        email = self.data['email']
        user = User.objects.create_user(username = username, email = email, password = password)
        user.is_active = True
        user.save()
        user = auth.authenticate(username = username, password = password)
        return user
