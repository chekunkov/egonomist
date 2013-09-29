from django.conf import settings
from django.conf.urls import patterns, include, url
from django.contrib import admin
from django.conf.urls.static import static


admin.autodiscover()

urlpatterns = patterns('',
    url(r'^$', 'egonomist.views.hello', name='home'),
    url(r'^admin/', include(admin.site.urls)),
    url(r'^complete/instagram/', 'egonomist.views.complete', name='complete'),
    url(r'^choose/', 'egonomist.views.choose', name='choose')
) + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
