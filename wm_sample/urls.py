try:
    from django.conf.urls import patterns, url, include
except ImportError:
    from django.conf.urls.defaults import patterns, url, include

from django.contrib.staticfiles.urls import staticfiles_urlpatterns
from django.contrib import admin

from views import *


admin.autodiscover()

urlpatterns = patterns(
    '',
    (r'^admin/', include(admin.site.urls)),
    (r'^webmoney/', include('webmoney.urls')),
)

urlpatterns += patterns(
    '',
    url(r'^success/$', success, name='wm_sample-success'),
    url(r'^fail/$', fail, name='wm_sample-fail'),
    url(r'^$', simple_payment, name='wm_sample-payment'),
)

urlpatterns += staticfiles_urlpatterns()
