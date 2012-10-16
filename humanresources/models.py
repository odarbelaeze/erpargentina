# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

from stocks.models import WareHouse

class Worker(User):
    warehouse = models.ForeignKey(WareHouse)
    sale_earn_rate = models.FloatField()
    payment_earn_rate = models.FloatField()

    warehouse.verbose_name= u'Bodega'
    sale_earn_rate.verbose_name = u'Comisión por ventas'
    payment_earn_rate.verbose_name = u'Comisión por abonos'
    
    class Meta:
        verbose_name = u'Trabajador'
        verbose_name_plural = u'Trabajadores'
        get_latest_by = 'user.name'

    def total_earnings  (self):
        total = self.earning_set.aggregate(models.Sum('amount'))['amount__sum']
        if total:
            return total
        else:
            return 0

    total_earnings.short_description = u'Comiciones'

    def total_sales(self):
        return sum([c.total_partial() for c in self.charge_set.all()])

    total_sales.short_description = u'Ventas'

    def total_payments(self):
        total = self.payment_set.aggregate(models.Sum('amount'))['amount__sum']
        if total:
            return total
        else:
            return 0

    total_payments.short_description = u'Abonos'

    def total_payings(self):
        total = self.paying_set.aggregate(models.Sum('amount'))['amount__sum']
        if total:
            return total
        else:
            return 0

    total_payings.short_description = u'Liquidaciones'

    def balance(self):
        return self.total_payments() - self.total_earnings() - self.total_payings()

    balance.short_description = u'Por liqidar'

    def __unicode__(self):
        return self.get_full_name()

class Paying(models.Model):
    worker = models.ForeignKey(Worker)
    date = models.DateTimeField(auto_now_add = True)
    amount = models.PositiveIntegerField()

    worker.verbose_name = u'Trabajador'
    date.verbose_name = u'Fecha'
    amount.verbose_name = u'Monto'

    class Meta:
        ordering = ['worker', '-date']
        verbose_name = u'Liquidación'
        verbose_name_plural = u'Liquidaciones'

    def __unicode__(self):
        return u'Liquidación del {s.date} por {s.amount}'.format(s = self)

class Earning(models.Model):
    worker = models.ForeignKey(Worker)
    date = models.DateTimeField(auto_now_add = True)
    amount = models.PositiveIntegerField()

    worker.verbose_name = u'Trabajador'
    date.verbose_name = u'Fecha'
    amount.verbose_name = u'Monto'

    class Meta:
        verbose_name = u'Comisión'
        verbose_name_plural = u'Comisiones'

    def __unicode__(self):
        return u'Comisión del {s.date} por {s.amount}'.format(s = self)