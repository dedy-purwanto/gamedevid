from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('posts.views',
    url(r'^new/$', 'new', name='new'),
    url(r'^edit/(?P<post_id>\d+)/$', 'edit', name='edit'),
    url(r'^view/(?P<post_id>\d+)/$', 'view', name='view'),
)
