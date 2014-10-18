from django.conf.urls import patterns, include, url
from django.contrib import admin

urlpatterns = patterns('',
    # Examples:
    # url(r'^$', 'test_driven.views.home', name='home'),
    # url(r'^blog/', include('blog.urls')),

    url(r'^admin/', include(admin.site.urls)),
    url(r'^$', 'lists.views.home_page', name='home'),
    url(r'^lists/(.+)/$', 'lists.views.the_best', name='the_best'),
    url(r'^lists/new$', 'lists.views.new_list', name='new_list'),
)
