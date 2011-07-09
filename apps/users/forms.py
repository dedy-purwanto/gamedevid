from django import forms
from django.contrib import auth

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
