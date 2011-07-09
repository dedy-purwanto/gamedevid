from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('posts.views',
    url(r'^new/$', 'new', name='new'),
)
