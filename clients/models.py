# coding=utf-8
from django.db import models

from humanresources.models import Worker
from humanresources.models import Earning
from stocks.models import Product

class Route(models.Model):

    name = models.CharField(max_length = 100)
    description = models.TextField(blank = True)
    in_charge = models.ForeignKey(Worker)

    name.verbose_name = u'Nombre'
    description.verbose_name = u'Descripción'
    in_charge.verbose_name = u'Encargado'

    class Meta:
        ordering = ['name']
        verbose_name = u'Ruta'
        verbose_name_plural = u'Rutas'

    def __unicode__(self):
        return self.name

class Client(models.Model):
    route = models.ForeignKey(Route)
    order = models.PositiveIntegerField(default = 0, blank = True, editable = False)
    full_name = models.CharField(max_length = 100)
    identification = models.CharField(max_length = 100, blank = True)
    addres = models.CharField(max_length = 200)
    indication = models.TextField(blank = True)
    phone_number = models.CharField(max_length = 100)
    alter_phone_number = models.CharField(max_length = 100, blank = True)

    route.verbose_name = u'Ruta'
    order.verbose_name = u'Posición'
    full_name.verbose_name = u'Nombre completo'
    identification.verbose_name = u'Identificación'
    addres.verbose_name = u'Dirección'
    indication.verbose_name = u'Indicación'
    phone_number.verbose_name = u'Número de teléfono'
    alter_phone_number.verbose_name = u'Tléfono alternativo'

    class Meta:
        ordering = ['route', 'order']
        verbose_name = u'Cliente'
        verbose_name_plural = u'Clientes'
        get_latest_by = 'route'
        unique_together = ('full_name', 'identification')

    def total_charges(self):
        return sum([c.total_partial() for c in self.charge_set.all()])

    total_charges.short_description = u'Total cargos'

    def total_payments(self):
        total = self.payment_set.aggregate(models.Sum('amount'))['amount__sum']
        if total:
            return total
        else:
            return 0

    total_payments.short_description = u'Total abonos'

    def total_debt(self):
        return self.total_charges() - self.total_payments()

    total_debt.short_description = u'Saldo'

    def has_cancelled(self):
        return self.total_debt() == 0

    has_cancelled.short_description = u'Ha cancelado?'
    has_cancelled.boolean = True

    def save(self, *args, **kwargs):
        if not self.id:
            qs = self.route.client_set.order_by('-order')
            try:
                self.order = qs[0].order + 1
            except IndexError:
                self.order = 0
        super(Client, self).save(*args, **kwargs)

    def _move(self, up):
        qs = self.route.client_set
        if up:
            qs = qs.order_by('-order').filter(order__lt = self.order)
        else:
            qs = qs.filter(order__gt = self.order)
        try:
            replacement = qs[0]
        except IndexError:
            # already first/last
            return
        self.order, replacement.order = replacement.order, self.order
        self.save()
        replacement.save()
    
    def move_down(self):
        """
        Move this object down one position.
        """
        return self._move(up = False)
    
    def move_up(self):
        """
        Move this object up one position.
        """
        return self._move(up = True)

    def __unicode__(self):
        return self.full_name
    
class Charge(models.Model):
    client = models.ForeignKey(Client)
    vendor = models.ForeignKey(Worker)
    quantity = models.PositiveIntegerField()
    product = models.ForeignKey(Product)
    price = models.PositiveIntegerField()

    client.verbose_name = u'Cliente'
    vendor.verbose_name = u'Vendedor'
    quantity.verbose_name = u'Cantidad'
    product.verbose_name = u'Producto'
    price.verbose_name = u'Precio'

    class Meta:
        verbose_name = u'Item de venta'
        verbose_name_plural = u'Items de venta'
    
    def total_partial(self):
        return self.quantity * self.price

    total_partial.short_description = u'Subtotal'

    def save(self, *args, **kwargs):
        if not self.id:
            # Reduce stocks
            try:
                st = self.vendor.warehouse.stock_set.get(product = self.product)
                st.level -= self.quantity
                if st.level < 0: return
                st.save_log(
                    u'Ajuste por Venta', 
                    u'Venta realizada por {s.vendor}, cantidad {s.quantity}'.format(s = self))
            except Exception, e:
                return
            # Generate earnings
            earn = self.total_partial() * self.vendor.sale_earn_rate / 100.0
            self.vendor.earning_set.add(Earning(amount = earn))
            print "Savig charge for the very first time."
        else:
            try:
                st = self.vendor.warehouse.stock_set.get(product = self.product)
                old = self.__class__.objects.get(id = self.id)
                st.level += old.quantity
                st.level -= self.quantity
                if st.level < 0: return
                st.save_log(
                    u'Ajuste por modificación en venta Venta', 
                    u'Venta realizada por {s.vendor}, cantidad {s.quantity}'.format(s = self))
            except Exception, e:
                return
            # change stocks

        super(Charge, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"{s.quantity} de {s.product}".format(s = self)


class Payment(models.Model):
    
    PTYPE_CHOICES = (
        ('initial', 'Cuota inicial'),
        ('payment', 'Abono'),
    )

    client = models.ForeignKey(Client)
    date = models.DateTimeField()
    collector = models.ForeignKey(Worker)
    p_type = models.CharField(
        choices = PTYPE_CHOICES, 
        default = 'payment', 
        max_length = 100
    )
    amount = models.PositiveIntegerField()

    client.verbose_name = u'Cliente'
    date.verbose_name = u'Fecha'
    collector.verbose_name = u'Cobrador'
    p_type.verbose_name = u'Tipo de abono'
    amount.verbose_name = u'Monto'

    class Meta:
        ordering = ['client', '-date']
        verbose_name = u'Abono'
        verbose_name_plural = u'Abonos'

    def save(self, *args, **kwargs):
        if self.amount > self.client.total_debt(): return
        if not self.id and self.p_type == 'payment':
            # Reduce stocks
            # Generate earnings
            earn = self.amount * self.collector.payment_earn_rate / 100.0
            self.collector.earning_set.add(Earning(amount = earn))
            print "Savig payment for the very first time."

        super(Payment, self).save(*args, **kwargs)

    def __unicode__(self):
        return u"Abono de {s.client} por {s.amount}".format(s = self)