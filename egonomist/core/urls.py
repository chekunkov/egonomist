from django.conf.urls import patterns, include, url
from django.contrib import admin


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'egonomist.views.hello', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^complete/instagram/', 'egonomist.views.complete', name='complete')
)
