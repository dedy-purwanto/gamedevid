from django.http import HttpResponse
from django.contrib.auth.decorators import login_required

from .forms import PostForm

@login_required
def new(request):
    form = PostForm(request.POST or None, author = request.user)
    if form.is_valid():
        form.save()
        return HttpResponse(status = 200)
