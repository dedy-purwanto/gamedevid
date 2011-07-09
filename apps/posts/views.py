from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .models import Post
from .forms import PostForm

@login_required
def new(request):
    form = PostForm(request.POST or None, author = request.user)
    if form.is_valid():
        form.save()
        return HttpResponse(status = 200)

@login_required
def edit(request, post_id):
    try:
        post = Post.objects.get(pk = post_id)
    except:
        return HttpResponse(status = 404)
    
    form = PostForm(request.POST or None, instance = post, author = request.user)
    if request.POST:
        if form.is_valid():
            form.save()
            return HttpResponse(status = 200)
        else:
            return HttpResponse(status = 500)
