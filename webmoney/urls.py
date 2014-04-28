try:
    from django.conf.urls import patterns, url
except ImportError:
    from django.conf.urls.defaults import patterns, url

from webmoney.views import result

urlpatterns = patterns(
    '',
    url(r'^result/$', result, name='webmoney-result'),
)
