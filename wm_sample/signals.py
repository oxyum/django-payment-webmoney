
from webmoney.signals import webmoney_payment_accepted


def webmoney_payment_accepted_processor(sender, payment, **kwargs):
    print payment
webmoney_payment_accepted.connect(webmoney_payment_accepted_processor, sender=None)
