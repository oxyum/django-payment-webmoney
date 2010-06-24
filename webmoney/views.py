
try:
    from hashlib import md5
except ImportError:
    from md5 import md5

from django.core.exceptions import ObjectDoesNotExist
from django.core.mail import mail_admins
from django.http import HttpResponse, HttpResponseBadRequest, HttpResponseNotAllowed
from django.views.decorators.csrf import csrf_exempt

from webmoney.forms import PrerequestForm, PaymentNotificationForm
from webmoney.models import Invoice, Payment, Purse
from webmoney.signals import webmoney_payment_accepted


@csrf_exempt
def result(request):

    if request.method != 'POST':
        return HttpResponseNotAllowed(permitted_methods=('POST',))
        
    form = PrerequestForm(request.POST)
    if form.is_valid() and form.cleaned_data['LMI_PREREQUEST']:
        payment_no = int(form.cleaned_data['LMI_PAYMENT_NO'])
        try:
            invoice = Invoice.objects.get(payment_no=payment_no)
        except ObjectDoesNotExist:
            return HttpResponseBadRequest("Invoice with number %s not found." % payment_no)
        return HttpResponse("YES")

    form = PaymentNotificationForm(request.POST)
    if form.is_valid():

        purse = Purse.objects.get(purse=form.cleaned_data['LMI_PAYEE_PURSE'])

        key = "%s%s%s%s%s%s%s%s%s%s" % (purse.purse,
                                        form.cleaned_data['LMI_PAYMENT_AMOUNT'],
                                        form.cleaned_data['LMI_PAYMENT_NO'],
                                        form.cleaned_data['LMI_MODE'],
                                        form.cleaned_data['LMI_SYS_INVS_NO'],
                                        form.cleaned_data['LMI_SYS_TRANS_NO'], 
                                        form.cleaned_data['LMI_SYS_TRANS_DATE'].strftime('%Y%m%d %H:%M:%S'),
                                        purse.secret_key,
                                        form.cleaned_data['LMI_PAYER_PURSE'],
                                        form.cleaned_data['LMI_PAYER_WM'])

        generated_hash = md5(key).hexdigest().upper()

        if generated_hash == form.cleaned_data['LMI_HASH']:
            payment = Payment(payee_purse=purse,
                              amount=form.cleaned_data['LMI_PAYMENT_AMOUNT'],
                              payment_no=form.cleaned_data['LMI_PAYMENT_NO'],
                              mode=form.cleaned_data['LMI_MODE'],
                              sys_invs_no=form.cleaned_data['LMI_SYS_INVS_NO'],
                              sys_trans_no=form.cleaned_data['LMI_SYS_TRANS_NO'],
                              sys_trans_date=form.cleaned_data['LMI_SYS_TRANS_DATE'],
                              payer_purse=form.cleaned_data['LMI_PAYER_PURSE'],
                              payer_wm=form.cleaned_data['LMI_PAYER_WM'],
                              paymer_number=form.cleaned_data['LMI_PAYMER_NUMBER'],
                              paymer_email=form.cleaned_data['LMI_PAYMER_EMAIL'],
                              telepat_phonenumber=form.cleaned_data['LMI_TELEPAT_PHONENUMBER'],
                              telepat_orderid=form.cleaned_data['LMI_TELEPAT_ORDERID'],
                              payment_creditdays=form.cleaned_data['LMI_PAYMENT_CREDITDAYS']
                              )
            try:
                invoice = Invoice.objects.get(payment_no=form.cleaned_data['LMI_PAYMENT_NO'])
                payment.invoice = invoice
            except ObjectDoesNotExist:
                mail_admins('Unprocessed payment without invoice!',
                            'Payment NO is %s.' % payment_no,
                            fail_silently=True)

            payment.save()

            webmoney_payment_accepted.send(sender=payment.__class__, payment=payment)
            return HttpResponse("OK")
        else:
            mail_admins('Unprocessed payment with incorrect hash!',
                        'Payment NO is %s.' % payment_no,
                        fail_silently=True)
            return HttpResponseBadRequest("Incorrect hash")

    return HttpResponseBadRequest("Unknown error!")
