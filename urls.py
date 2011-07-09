from django.conf.urls.defaults import patterns, include, url

# Uncomment the next two lines to enable the admin:
from django.contrib import admin
admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', include('home.urls', namespace='home')),   
    url(r'^users/', include('users.urls', namespace='users')),   
    url(r'^posts/', include('posts.urls', namespace='posts')),   

    url(r'^admin/', include(admin.site.urls)),
    url(r'^sentry/', include('sentry.web.urls')),
)
