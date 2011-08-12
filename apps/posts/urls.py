from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('posts.views',
    url(r'^new/$', 'new', name='new'),
    url(r'^new/(?P<parent_id>\d+)/$', 'new', name='new_reply'),
    url(r'^edit/(?P<post_id>\d+)/$', 'edit', name='edit'),
    url(r'^view/(?P<post_id>\d+)/(?P<slug>[-\w]+)/$', 'view', name='view'),
    url(r'^recent-threads/$', 'list_recent_threads', name='list_recent_threads'),
)
