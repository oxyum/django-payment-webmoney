
from django import forms
from django.utils.translation import ugettext_lazy as _

from webmoney import PURSE_RE, WMID_RE

class PaymentRequestForm(forms.Form):
    LMI_PAYMENT_AMOUNT = forms.DecimalField(max_digits=7, decimal_places=2, label=_(u'Amount'))
    LMI_PAYMENT_DESC = forms.CharField(label=_(u'Description'), widget=forms.HiddenInput())
    LMI_PAYMENT_NO = forms.IntegerField(label=_(u'Payment Number'), widget=forms.HiddenInput())
    LMI_PAYEE_PURSE = forms.RegexField(regex=PURSE_RE, widget=forms.HiddenInput())
    LMI_SIM_MODE = forms.IntegerField(initial="0", widget=forms.HiddenInput())

class PrerequestForm(forms.Form):

    LMI_PREREQUEST = forms.BooleanField(label=_('Prerequest flag'), required=False)
    LMI_PAYEE_PURSE = forms.RegexField(regex=PURSE_RE)

    LMI_PAYMENT_AMOUNT = forms.DecimalField(max_digits=7, decimal_places=2, label=_(u'Amount'))
    LMI_PAYMENT_NO = forms.IntegerField(label=_(u'Payment Number'))
    LMI_MODE = forms.IntegerField(label=_('Test mode'), min_value=0, max_value=1)

    LMI_PAYER_WM = forms.RegexField(regex=WMID_RE)
    LMI_PAYER_PURSE = forms.RegexField(regex=PURSE_RE)

    # Paymer
    LMI_PAYMER_NUMBER = forms.CharField()
    LMI_PAYMER_EMAIL = forms.EmailField()

    # Telepat
    LMI_TELEPAT_PHONENUMBER = forms.CharField()
    LMI_TELEPAT_ORDERID = forms.CharField()

    # Credit
    LMI_PAYMENT_CREDITDAYS = forms.IntegerField(min_value=0)

class PaymentNotificationForm(PrerequestForm):
    LMI_SYS_INVS_NO = forms.IntegerField()
    LMI_SYS_TRANS_NO = forms.IntegerField()
    LMI_HASH = forms.CharField()
    LMI_SYS_TRANS_DATE = forms.DateTimeField(input_formats='%Y%m%d %H:%M:%S')

    # Please do not USE IT!!! Security flaw!
    # LMI_SECRET_KEY

class SettledPaymentForm(forms.Form):
    LMI_PAYMENT_NO = forms.IntegerField(label=_(u'Payment Number'))
    LMI_SYS_INVS_NO = forms.IntegerField()
    LMI_SYS_TRANS_NO = forms.IntegerField()
    LMI_SYS_TRANS_DATE = forms.DateTimeField(input_formats='%Y%m%d %H:%M:%S')

class UnSettledPaymentForm(SettledPaymentForm):
    pass
