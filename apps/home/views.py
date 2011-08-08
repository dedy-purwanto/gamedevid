from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage

from posts.models import Post
from tags.models import Tag
from games.models import Game

#Home is just a home, its just a single page that combines everything
#Please separate another page into a single app instead
def home(request):
    latest_games = Game.objects.all().order_by('-id')[:5]
    context = {
                'latest_games' : latest_games
              }

    return render_to_response(
                                "home/home.html",
                                context,
                                RequestContext(request)
                             )
