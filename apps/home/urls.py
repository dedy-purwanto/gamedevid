from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('home.views',
    url(r'^$', 'home', name='home'),
)
