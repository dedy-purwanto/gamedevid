from .models import Post
def fetch_latest_posts(request):
    return {
        'global_latest_posts' : Post.get_latests()[:20],
    }
