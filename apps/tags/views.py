# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from .models import Tag,TagPost
from posts.models import Post
def tag_post_list(request, tag_id, slug):
    tag = get_object_or_404(Tag, pk = tag_id)
    tag_post = TagPost.objects.filter(tag = tag).order_by('-post__date_sorted')
    tag_post.query.group_by = ['post_id']
    post_list = [tp.post for tp in tag_post]
    paginator = Paginator(post_list, 40)
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
                'posts' : posts,
              }

    return render_to_response(
                                "tags/tag_post_list.html",
                                context,
                                RequestContext(request)
                             )
    
