from django.conf.urls.defaults import patterns, include, url

urlpatterns = patterns('users.views',
    url(r'^login/$', 'login', name='login'),
    url(r'^logout/$', 'logout', name='logout'),
    url(r'^register/$', 'register', name='register'),
    url(r'^edit_profile/$', 'edit_profile', name='edit_profile'),
)
