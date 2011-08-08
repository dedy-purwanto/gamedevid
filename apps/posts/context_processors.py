from .models import Post
def fetch_latest_posts(request):
    try:
        random_image = Post.objects.exclude(image = None).order_by('?')[0]
    except Post.DoesNotExist:
        random_image = None
    return {
        'global_latest_posts' : Post.get_latests()[:20],
        'random_image' : random_image,
    }
