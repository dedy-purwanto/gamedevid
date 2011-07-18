from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('tags.views',
    url(r'^(?P<tag_id>\d+)/(?P<slug>[-\w]+)/$', 'tag_post_list', name='tag_post_list'),
)
