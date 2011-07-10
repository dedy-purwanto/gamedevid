from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from .models import Post
from .forms import PostForm

@login_required
def new(request, parent_id = None):
    parent = None
    if parent_id:
        parent = get_object_or_404(Post, pk = parent_id)
    form = PostForm(request.POST or None, author = request.user, parent = parent)
    if form.is_valid():
        post = form.save()
        return redirect(reverse("posts:view", args=[post.id if parent_id is None else parent_id, post.title_slug()])) 
    context = {
                'form' : form,
              }

    return render_to_response(
                                "posts/post_form.html",
                                context,
                                RequestContext(request)
                             )
@login_required
def edit(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    
    form = PostForm(request.POST or None, instance = post, author = request.user)
    if form.is_valid():
        form.save()
        
        return redirect(reverse("posts:view", args=[post.id if post.parent is None else post.parent.id, post.title_slug()])) 
    context = {
                'form' : form,
              }

    return render_to_response(
                                "posts/post_form.html",
                                context,
                                RequestContext(request)
                             )
def view(request, post_id, slug):
    post = get_object_or_404(Post, pk = post_id)
    context = {
                'post' : post,
              }

    return render_to_response(
                                "posts/view_main.html",
                                context,
                                RequestContext(request)
                             )

