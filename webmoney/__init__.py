
import re

from django.core.exceptions import ImproperlyConfigured
from django.conf import settings

from webmoney import signals

_err_msg = "You need to specify %s in your Django settings file."

if not hasattr(settings, 'MERCHANT_WM_PAYEE_PURSE'):
    raise ImproperlyConfigured(_err_msg % 'MERCHANT_WM_PAYEE_PURSE')

if not hasattr(settings, 'MERCHANT_WM_SECRET_KEY'):
    raise ImproperlyConfigured(_err_msg % 'MERCHANT_WM_SECRET_KEY')

if not getattr(settings, 'MERCHANT_WM_USE_SIMPLE_PAYMENT', False):
    raise ImproperlyConfigured("Only simple payment mode supported in this version. "
                               "You must set %s to True." % 'MERCHANT_WM_USE_SIMPLE_PAYMENT')

PURSE_RE = re.compile(ur'^(?P<type>[ZREUYBGDC])(?P<number>\d{12})$')
WMID_RE = re.compile(ur'^\d{12}$')
