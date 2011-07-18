# Create your views here.
from django.shortcuts import render_to_response, get_object_or_404
from django.template import RequestContext
from .models import Tag,TagPost

def tag_post_list(request, tag_id, slug):
    tag = get_object_or_404(Tag, pk = tag_id)
    tag_post = TagPost.objects.filter(tag = tag).order_by('-post__date_created')
    tag_post.query.group_by = ['post_id']
    post = [tp.post for tp in tag_post]
    context = {
                'post' : post,
              }

    return render_to_response(
                                "tags/tag_post_list.html",
                                context,
                                RequestContext(request)
                             )
    
