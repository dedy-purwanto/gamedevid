from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.shortcuts import redirect
from django.core.files.base import ContentFile
from django.core.urlresolvers import reverse
from .models import Post, PostReader
from images.forms import ImageForm
from games.forms import GameForm
from .forms import PostForm
from tags.forms import TagForm


@login_required
def new(request, parent_id = None):
    parent = None
    if parent_id:
        parent = get_object_or_404(Post, pk = parent_id)
    form = PostForm(
        request.POST or None,
        request.FILES or None,
        author = request.user, 
        parent = parent,
    )

    image_form = ImageForm(request.POST or None, request.FILES or None)
    game_form = GameForm(request.POST or None, request.FILES or None)

    tag_form = TagForm(request.POST or None) if parent is None else None

    valid = False
    
    #A reply
    if parent is not None:
        valid = (parent is not None and form.is_valid())
    
    #a new post:
    if parent is None:
        valid = (parent is None and form.is_valid() and tag_form.is_valid())
    
    #an image post:
    if request.GET.get('image',False):
        valid = (parent is None and form.is_valid() and tag_form.is_valid() and image_form.is_valid())

    #a game post:
    if request.GET.get('game',False):
        valid = (parent is None and form.is_valid() and tag_form.is_valid() and game_form.is_valid())

    if valid:       
        post = form.save()
        if parent is None:
            tag_form.post = post
            tag_form.save()
        
        if parent is None:
            PostReader.clear(post = post)
        else:
            PostReader.clear(post = post.parent)
        
        if image_form.is_valid():
            image_form.save(post = post)
        
        if game_form.is_valid():
            game_form.save(post = post)
            game_form.save_m2m()

        r_post = post if not parent else parent
        return redirect(reverse("posts:view", args=[r_post.id, r_post.title_slug()])) 
    context = {
                'form' : form,
                'tag_form' : tag_form,
                'image_form' : image_form,
                'game_form' : game_form,
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

    reply_form = PostForm(author = request.user, quick_reply = True) # No need to get anything here, coz it'll be redirected to reply page

    if request.user.is_authenticated():
        PostReader.add(user = request.user, post = post if post.parent is not None else post)

    context = {
                'post' : post,
                'reply_form' : reply_form,
              }

    return render_to_response(
                                "posts/view_main.html",
                                context,
                                RequestContext(request)
                             )
