from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from posts.models import Post
from tags.models import Tag

#Home is just a home, its just a single page that combines everything
#Please separate another page into a single app instead
def home(request):
    posts_latests = Post.get_latests()
    paginator = Paginator(posts_latests, 10)
    try:
        page = int(request.GET.get('page','1'))
        posts = paginator.page(page)
    except ValueError:
        page = 1
    
    try:
        posts = paginator.page(page)
    except (EmptyPage,InvalidPage):
        posts = paginator.page(paginator.num_pages)

    context = {
                'posts_latests' : posts,
              }

    return render_to_response(
                                "home/home.html",
                                context,
                                RequestContext(request)
                             )
