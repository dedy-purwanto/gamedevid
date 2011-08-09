from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.urlresolvers import reverse
from django.shortcuts import redirect
from django.contrib import auth
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout as logout_user
from .forms import LoginForm, RegisterForm
from avatars.forms import AvatarForm
def login(request):
    form = LoginForm(request.POST or None)
    if form.is_valid():
        next_url = request.GET.get('next', "/")
        user = form.save()
        auth.login(request, user)
        return redirect(next_url)
    context = {
                'form' : form,
              }

    return render_to_response(
                                "users/login.html",
                                context,
                                RequestContext(request)
                             )
@login_required
def edit_profile(request):
    avatar_form = AvatarForm(request.POST or None, request.FILES or None)
    #for now this is okay, if later on we have multiple form, we'll need to update this
    if avatar_form.is_valid():
        avatar_form.save(user = request.user)
        next_url = request.GET.get('next', reverse('users:edit_profile'))
        return redirect(next_url)
    context = {
                'avatar_form' : avatar_form,
              }

    return render_to_response(
                                "users/edit_profile.html",
                                context,
                                RequestContext(request)
                             )

    

@login_required
def logout(request):
    logout_user(request)
    next_url = request.GET.get('next', "/")
    return redirect(next_url)
def register(request):
    form = RegisterForm(request.POST or None)
    if form.is_valid():
        next_url = request.GET.get('next', "/")
        user = form.save()
        auth.login(request, user)
        return redirect(next_url)
    context = {
                'form' : form,
              }

    return render_to_response(
                                "users/register.html",
                                context,
                                RequestContext(request)
                             )

