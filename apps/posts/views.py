from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.shortcuts import redirect
from django.core.urlresolvers import reverse
from .models import Post, PostReader
from .forms import PostForm
from tags.forms import TagForm

@login_required
def new(request, parent_id = None):
    parent = None
    if parent_id:
        parent = get_object_or_404(Post, pk = parent_id)
    form = PostForm(request.POST or None, author = request.user, parent = parent)
    tag_form = TagForm(request.POST or None) if parent is None else None
    if (parent is not None and form.is_valid()) or (parent is None and form.is_valid() and tag_form.is_valid()):
        post = form.save()
        if parent is None:
            tag_form.post = post
            tag_form.save()

        r_post = post if not parent else parent
        return redirect(reverse("posts:view", args=[r_post.id, r_post.title_slug()])) 
    context = {
                'form' : form,
                'tag_form' : tag_form,
              }

    return render_to_response(
                                "posts/post_form.html",
                                context,
                                RequestContext(request)
                             )
@login_required
def edit(request, post_id):
    post = get_object_or_404(Post, pk = post_id)
    parent = post.parent
    form = PostForm(request.POST or None, instance = post, author = request.user)
    tag_form = TagForm(request.POST or None, post = post) if parent is None else None
    if (parent is not None and form.is_valid()) or (parent is None and form.is_valid() and tag_form.is_valid()):
        form.save()
        if parent is None:
            tag_form.save()
        r_post = post if not post.parent else post.parent
        return redirect(reverse("posts:view", args=[r_post.id, r_post.title_slug()])) 
    context = {
                'form' : form,
                'tag_form' : tag_form,
              }

    return render_to_response(
                                "posts/post_form.html",
                                context,
                                RequestContext(request)
                             )

def view(request, post_id, slug):
    post = get_object_or_404(Post, pk = post_id)

    if request.user.is_authenticated():
        PostReader.add(user = request.user, post = post if post.parent is not None else post)

    context = {
                'post' : post,
              }

    return render_to_response(
                                "posts/view_main.html",
                                context,
                                RequestContext(request)
                             )
