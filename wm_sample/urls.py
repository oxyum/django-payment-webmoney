from django.conf.urls.defaults import *
from django.contrib import admin

from views import *


admin.autodiscover()

urlpatterns = patterns('',
    (r'^admin/', include(admin.site.urls)),
)

urlpatterns += patterns('',
    url(r'^success/$', success,        name='wm_sample-success'),
    url(r'^fail/$',    fail,           name='wm_sample-fail'),
    url(r'^$',         simple_payment, name='wm_sample-payment'),
)
