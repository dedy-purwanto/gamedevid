from django.http import HttpResponse
from django.contrib import auth
from .forms import LoginForm

def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        user = form.save()
        auth.login(request, user)
        return HttpResponse(status = 200)

