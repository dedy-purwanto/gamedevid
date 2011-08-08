from .models import Image
def fetch_random_image(request):
    try:
        random_image = Image.objects.all().order_by('?')
        if random_image.count() > 0:
            random_image = random_image[0]
    except Image.DoesNotExist:
        random_image = None
    return {
        'random_image' : random_image,
    }
