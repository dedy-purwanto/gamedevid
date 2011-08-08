from posts.models import Post
def fetch_random_image(request):
    try:
        random_image = Post.objects.exclude(image = None).order_by('?')
        if random_image.count() > 0:
            random_image = random_image[0]
    except Post.DoesNotExist:
        random_image = None
    return {
        'random_image' : random_image,
    }
