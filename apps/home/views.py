from django.http import HttpResponse
from django.shortcuts import render_to_response
from django.template import RequestContext
from django.core.paginator import Paginator, InvalidPage, EmptyPage
from django.db.models import Q
from posts.models import Post
from announcements.models import Announcement
from tags.models import Tag
from games.models import Game

#Home is just a home, its just a single page that combines everything
#Please separate another page into a single app instead
def home(request):
    latest_games = Game.objects.all().order_by('-id')[:4]
    latest_showcases = Post.objects.exclude(Q(image = None) & Q(game = None)).order_by('-id')[:20]

    latest_announcements = Post.objects.exclude(announcement = None).order_by('-id')
    if latest_announcements.count() > 0:
        latest_announcements = latest_announcements[:5]

    context = {
                'latest_games' : latest_games,
                'latest_showcases' : latest_showcases,
                'latest_announcements' : latest_announcements,

    }

    return render_to_response(
                                "home/home.html",
                                context,
                                RequestContext(request)
                             )
