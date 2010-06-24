
from django.conf.urls.defaults import *

from webmoney.views import result

urlpatterns = patterns('',
    url(r'^result/$', result, name='webmoney-result'),
)
