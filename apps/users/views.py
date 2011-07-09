from django.http import HttpResponse
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import auth
from .forms import LoginForm

def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        next_url = request.GET.get('next', reverse("home:home"))
        user = form.save()
        auth.login(request, user)
        return redirect(next_url)

