# coding=utf-8
from django.db import models
from django.contrib.auth.models import User

class Worker(User):
    sale_earn_rate = models.FloatField()
    payment_earn_rate = models.FloatField()

    sale_earn_rate.verbose_name = "Comisión por ventas"
    payment_earn_rate.verbose_name = "Comisión por abonos"
    
    class Meta:
        verbose_name = "Trabajador"
        verbose_name_plural = "Trabajadores"
        get_latest_by = 'user.name'

    def __unicode__(self):
        return self.get_full_name()

class Paying(models.Model):
    worker = models.ForeignKey(Worker)
    date = models.DateTimeField(auto_now_add = True)
    ammount = models.PositiveIntegerField()

    worker.verbose_name = "Trabajador"
    date.verbose_name = "Fecha"
    ammount.verbose_name = "Monto"

    class Meta:
        ordering = ['worker', '-date']
        verbose_name = "Liquidación"
        verbose_name_plural = "Liquidaciones"

    def __unicode__(self):
        return "Liquidación del {s.date} por {s.ammount}".format(s = self)

class Earning(models.Model):
    worker = models.ForeignKey(Worker)
    date = models.DateTimeField(auto_now_add = True)
    ammount = models.PositiveIntegerField()

    worker.verbose_name = "Trabajador"
    date.verbose_name = "Fecha"
    ammount.verbose_name = "Monto"

    class Meta:
        verbose_name = "Comisión"
        verbose_name_plural = "Comisiones"

    def __unicode__(self):
        return "Comisión del {s.date} por {s.ammount}".format(s = self)