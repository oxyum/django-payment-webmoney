from django.template import loader, RequestContext
from wm_sample.helpers import render_to

from webmoney.forms import *
from webmoney.models import Invoice, Purse


@render_to('wm_sample/simple_payment.html')
def simple_payment(request):
    response = {}

    initial = {
        'LMI_PAYEE_PURSE': Purse.objects.all()[0],
        'LMI_PAYMENT_NO': Invoice.objects.create(user=request.user).payment_no,
        'LMI_PAYMENT_DESC': loader.render_to_string('wm_sample/simple_payment_desc.txt',
                                                    RequestContext(request)).strip()[:255],
    }

    response['form'] = PaymentRequestForm(initial=initial)

    return response

@render_to('wm_sample/success.html')
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

@render_to('wm_sample/fail.html')
def fail(request):
    response = {}
    if request.method == 'POST':
        form = UnSettledPaymentForm(request.POST)
        if form.is_valid():
            response['id'] = form.cleaned_data['LMI_PAYMENT_NO']
            response['sys_invs_no'] = form.cleaned_data['LMI_SYS_INVS_NO']
            response['sys_trans_no'] = form.cleaned_data['LMI_SYS_TRANS_NO']
            response['date'] = form.cleaned_data['LMI_SYS_TRANS_DATE']

    return response
