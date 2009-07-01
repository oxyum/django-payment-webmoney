
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from random import choice
from string import digits
from decimal import Decimal

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import mail_admins
from django.utils.translation import ugettext_lazy as _
from django.http import HttpResponse, HttpResponseNotAllowed
from django.conf import settings
from django.template import loader, RequestContext

from django.contrib.auth.decorators import login_required

from webmoney.forms import *
from webmoney.helpers import render_to
from webmoney.models import Invoice, Payment
from webmoney.signals import webmoney_payment_accepted

@login_required
@render_to('webmoney/simple_payment.html')
def simple_payment(request):
    response = {}

    initial = {
        'LMI_PAYEE_PURSE': settings.MERCHANT_WM_PAYEE_PURSE,
        'LMI_PAYMENT_NO': Invoice.objects.create(user=request.user).payment_no,
        'LMI_PAYMENT_DESC': loader.render_to_string('webmoney/simple_payment_desc.txt',
                                                    RequestContext(request)).strip()[0:255],
    }

    response['form'] = PaymentRequestForm(initial=initial)

    return response

@render_to('webmoney/success.html')
def success(request):
    response = {}

    if request.method == 'POST':
        form = SettledPaymentForm(request.POST)
        if form.is_valid():
            response['id'] = form.cleaned_data['LMI_PAYMENT_NO']
            response['sys_invs_no'] = form.cleaned_data['LMI_SYS_INVS_NO']
            response['sys_trans_no'] = form.cleaned_data['LMI_SYS_TRANS_NO']
            response['date'] = form.cleaned_data['LMI_SYS_TRANS_DATE']

    return response


@render_to('webmoney/failure.html')
def failure(request):
    response = {}
    if request.method == 'POST':
        form = UnSettledPaymentForm(request.POST)
        if form.is_valid():
            response['id'] = form.cleaned_data['LMI_PAYMENT_NO']
            response['sys_invs_no'] = form.cleaned_data['LMI_SYS_INVS_NO']
            response['sys_trans_no'] = form.cleaned_data['LMI_SYS_TRANS_NO']
            response['date'] = form.cleaned_data['LMI_SYS_TRANS_DATE']
    return response


def result(request):
    if request.method == 'POST':
        
        form = PrerequestForm(request.POST)
        if form.is_valid() and form.cleaned_data['LMI_PREREQUEST']:
            payment_no = int(form.cleaned_data['LMI_PAYMENT_NO'])
            try:
                invoice = Invoice.objects.get(payment_no=payment_no)
                
            except ObjectDoesNotExist:
                return HttpResponse("Invoice with number %s not found." % payment_no)
            return HttpResponse("YES")

        form = PaymentNotificationForm(request.POST)
        if form.is_valid():

            payment_no = form.cleaned_data['LMI_PAYMENT_NO']
            payee_purse = form.cleaned_data['LMI_PAYEE_PURSE']
            payer_wm = form.cleaned_data['LMI_PAYER_WM']
            payer_purse = form.cleaned_data['LMI_PAYER_PURSE']
            amount = form.cleaned_data['LMI_PAYMENT_AMOUNT']
            mode = form.cleaned_data['LMI_MODE']
            sys_invs_no = form.cleaned_data['LMI_SYS_INVS_NO']
            sys_trans_no = form.cleaned_data['LMI_SYS_TRANS_NO']
            sys_trans_date = form.cleaned_data['LMI_SYS_TRANS_DATE'].strftime('%Y%m%d %H:%M:%S')
            wm_hash = form.cleaned_data['LMI_HASH']

            key = "%s%s%s%s%s%s%s%s%s%s" % (payee_purse, amount, payment_no, mode, sys_invs_no, sys_trans_no, 
                                            sys_trans_date, settings.MERCHANT_WM_SECRET_KEY, payer_purse, payer_wm)

            generated_hash = md5(key).hexdigest().upper()

            if generated_hash == wm_hash:
                payment = Payment(payee_purse=payee_purse,
                                  amount=amount,
                                  payment_no=payment_no,
                                  mode=mode,
                                  sys_invs_no=sys_invs_no,
                                  sys_trans_no=sys_trans_no,
                                  sys_trans_date=sys_trans_date,
                                  payer_purse=payer_purse,
                                  payer_wm=payer_wm,
                                  paymer_number=form.cleaned_data['LMI_PAYMER_NUMBER'],
                                  paymer_email=form.cleaned_data['LMI_PAYMER_EMAIL'],
                                  telepat_phonenumber=form.cleaned_data['LMI_TELEPAT_PHONENUMBER'],
                                  telepat_orderid=form.cleaned_data['LMI_TELEPAT_ORDERID'],
                                  payment_creditdays=form.cleaned_data['LMI_PAYMENT_CREDITDAYS']
                                  )
                try:
                    invoice = Invoice.objects.get(payment_no=payment_no)
                    payment.invoice = invoice
                except ObjectDoesNotExist:
                    mail_admins('Unprocessed payment without invoice!',
                                'Payment NO is %s.' % payment_no,
                                fail_silently=True)

                payment.save()

                webmoney_payment_accepted.send(sender=payment)

        else:
            return HttpResponseNotAllowed(permitted_methods=('POST',))

    return HttpResponse("OK")
