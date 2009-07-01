
from django.conf import settings
from django.conf.urls.defaults import *

from webmoney import views


urlpatterns = patterns('',
    url(r'^success/$', views.success, name='webmoney-success'),
    url(r'^failure/$', views.failure, name='webmoney-failure'),
    url(r'^result/$', views.result, name='webmoney-result'),
)

if not hasattr(settings, ''):

if getattr(settings, 'MERCHANT_WM_USE_SIMPLE_PAYMENT', False):
    urlpatterns += patterns('',
        url(r'^$', views.simple_payment, name='simple_payment'),
    )
