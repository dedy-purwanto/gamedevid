from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('users.views',
    url(r'^login/$', 'login', name='login'),
)
