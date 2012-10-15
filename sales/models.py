from django.db import models

from clients.models import Client
from humanresources.models import Worker
from stocks.models import Product
    
class Sale(models.Model):
    client = models.ForeignKey(Client)
    vendor = models.ForeignKey(Worker)
    date = models.DateTimeField(auto_now_add = True)
    s_type = models.CharField(max_length = 100, blank = True)
    s_info = models.TextField(blank = True)

    client.verbose_name = "Cliente"
    vendor.verbose_name = "Vendedor"
    date.verbose_name = "Fecha"
    s_type.verbose_name = "Tipo de venta"
    s_info.verbose_name = "Informacion adicional"

    class Meta:
        verbose_name = "Venta"
        verbose_name_plural = "Ventas"

    def total(self):
        return self.tiketline_set.aggregate(models.Sum('total_partial'))['total_partial__sum']

    def balance(self):
        return self.total() - self.payment_set.aggregate(models.Sum('amount'))['amount__sum']

    def save(self, *args, **kwargs):
        super(Sale, self).save(*args, **kwargs)
    
    def __unicode__(self):
        return "Venta a {s.client} el {s.date}".format(s = self)

class TiketLine(models.Model):
    sale = models.ForeignKey(Sale)
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product)
    price = models.PositiveIntegerField()

    sale.verbose_name = "Venta"
    quantity.verbose_name = "Cantidad"
    product.verbose_name = "Producto"
    price.verbose_name = "Precio"

    class Meta:
        verbose_name = "Item de venta"
        verbose_name_plural = "Items de venta"
    
    def total_partial(self):
        return self.quantity * self.price

    total_partial.short_description = "Subtotal"

    def __unicode__(self):
        return "{s.quantity} de {s.product}".format(s = self)


class Payment(models.Model):
    sale = models.ForeignKey(Sale)
    date = models.DateTimeField()
    collector = models.ForeignKey(Worker)
    p_type = models.CharField(max_length = 100)
    amount = models.PositiveIntegerField()

    sale.verbose_name = "Venta"
    date.verbose_name = "Fecha"
    collector.verbose_name = "Cobrador"
    p_type.verbose_name = "Tipo de abono"
    amount.verbose_name = "Monto"

    class Meta:
        ordering = ['sale', '-date']
        verbose_name = "Abono"
        verbose_name_plural = "Abonos"

    def __unicode__(self):
        return "Abono de {s.sale.client} por {s.amount}".format(s = self)