from django.dispatch import Signal

webmoney_payment_accepted = Signal(providing_args=["payment"])
