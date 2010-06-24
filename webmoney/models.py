
from datetime import datetime, timedelta
from time import sleep

from django.core.exceptions import ObjectDoesNotExist
from django.db import IntegrityError, models, transaction

import signals


class Purse(models.Model):
    purse = models.CharField(max_length=13, unique=True)
    secret_key = models.CharField(max_length=50)

    def __unicode__(self):
        return '%s' % (self.purse, )

class Invoice(models.Model):
    user = models.ForeignKey('auth.User')
    created_on = models.DateTimeField(unique=True, editable=False)
    payment_no = models.PositiveIntegerField(unique=True, editable=False)

    def _is_payed_admin(self):
        try:
            self.payment
            return True
        except ObjectDoesNotExist:
            return False
    _is_payed_admin.boolean = True
    _is_payed_admin.short_description = 'is payed'
    _is_payed_admin.admin_order_field = 'payment'

    is_payed = property(_is_payed_admin)

    @transaction.commit_manually
    def save(self, force_insert=False, force_update=False, using=None):
        sid = transaction.savepoint()
        if self.pk is None:
            i = 1
            while self.pk is None:

                if i > 10:
                    sleep(0.001)

                if i > 20:
                    # Protection from infinite loop
                    raise IntegrityError('Too many iterations while generating unique Invoice number.')

                try:
                    self.created_on = datetime.utcnow()
                    self.created_on = self.created_on - timedelta(microseconds = self.created_on.microsecond % 100)

                    self.payment_no = (self.created_on.hour*3600+
                                       self.created_on.minute*60+
                                       self.created_on.second)*10000 + (self.created_on.microsecond // 100)
                    super(Invoice, self).save(force_insert, force_update)

                except IntegrityError:
                    transaction.savepoint_rollback(sid)

                i += 1
        else:
            super(Invoice, self).save(force_insert, force_update)

        transaction.savepoint_commit(sid)
        transaction.commit()

    def __unicode__(self):
        return '%s/%s (for: %s)' % (self.payment_no, self.created_on.date(), self.user, )

PAYMENT_MODE_CHOICES = (
    (0, 'REAL'),
    (1, 'TEST'),
)

class Payment(models.Model):
    created_on = models.DateTimeField(auto_now_add=True, editable=False)

    invoice = models.OneToOneField(Invoice, blank=True, null=True, related_name='payment')

    payee_purse = models.ForeignKey(Purse, related_name='payments')

    amount = models.DecimalField(decimal_places=2, max_digits=9)

    payment_no = models.PositiveIntegerField(unique=True)

    mode = models.PositiveSmallIntegerField(choices=PAYMENT_MODE_CHOICES)

    sys_invs_no = models.PositiveIntegerField()
    sys_trans_no = models.PositiveIntegerField()
    sys_trans_date = models.DateTimeField()

    payer_purse = models.CharField(max_length=13)
    payer_wm = models.CharField(max_length=12)

    paymer_number = models.CharField(max_length=30, blank=True)
    paymer_email = models.EmailField(blank=True)

    telepat_phonenumber = models.CharField(max_length=30, blank=True)
    telepat_orderid = models.CharField(max_length=30, blank=True)

    payment_creditdays = models.PositiveIntegerField(blank=True, null=True)
    
    def __unicode__(self):
        return "%s - %s WM%s" % (self.payment_no, self.amount, self.payee_purse.purse[0])
