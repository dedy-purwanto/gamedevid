from .models import Tag
def list_sticky_tags(request):
    return {
        'global_sticky_tags' : Tag.tree.all()
    }
