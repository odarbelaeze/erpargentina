# coding=utf-8
from django.db import models
from django.core.validators import RegexValidator
from django.core.exceptions import ObjectDoesNotExist


class WareHouse(models.Model):
    """docstring for WareHouse"""
    name = models.CharField(max_length = 255, unique = True)
    address = models.CharField(max_length = 255, unique = True)
    more_info = models.TextField(blank = True)
    
    name.verbose_name = "Nombre"
    address.verbose_name = "Dirección"
    more_info.verbose_name = "Mas información"

    class Meta():
        """docstring for Meta"""
        ordering = ['name']
        get_latest_by = 'id'
        verbose_name = "Bodega"
        verbose_name_plural = "Bodegas"

    def __unicode__(self):
        return self.name

class Product(models.Model):
    """docstring for Product"""
    name = models.CharField(max_length = 255, unique = True)
    description = models.TextField(blank = True)

    name.verbose_name = "Nombre"
    description.verbose_name = "Descipcion"

    class Meta():
        """docstring for Meta"""
        ordering = ['id']
        get_latest_by = 'id'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def has_description(self):
        return bool(self.description)

    def available(self, wh = None):
        return any([s.level > 0 for s in self.stock_set.all()])

    available.boolean = True
    available.short_description = "Producto disponible?"

    def stock_level(self):
        return sum([s.level for s in self.stock_set.all()])

    stock_level.integer = True
    stock_level.short_description = "Total unidades disponibles"

    def reference(self):
        return "{:05d}".format(self.id)

    reference.short_description = "Referencia"

    def price(self):
        pt = self.pricetag_set.latest()
        if pt:
            return pt.price
        else:
            return 0

    price.short_description = "Precio actual"

    def __unicode__(self):
        return self.name
    
class PriceTag(models.Model):
    """docstring for PriceTag"""
    date = models.DateTimeField(auto_now_add = True)
    product = models.ForeignKey(Product)
    price = models.PositiveIntegerField()

    date.verbose_name = "Fecha"
    product.verbose_name = "Producto"
    price.verbose_name = "Precio"

    class Meta():
        """docstring for Meta"""
        ordering = ['product', '-date']
        get_latest_by = 'date'
        verbose_name = "Precio"
        verbose_name_plural = "Precios"

    def __unicode__(self):
        return "Precio de {.product:s}".format(self)

class Stock(models.Model):
    """docstring for Stock"""
    warehouse = models.ForeignKey(WareHouse)
    product = models.ForeignKey(Product)
    level = models.PositiveIntegerField(default = 0)

    warehouse.verbose_name = "Bodega"
    product.verbose_name = "Producto"
    level.verbose_name = "Cantidad"

    class Meta():
        """docstring for Meta"""
        ordering = ['warehouse', 'product']
        get_latest_by = 'id'
        verbose_name = "Existencia"
        verbose_name_plural = "Existencias"
        unique_together = ('warehouse', 'product')

    def save_log(self, reason, description = "", *args, **kwargs):
        super(Stock, self).save(*args, **kwargs)
        StockEvent(stock = self, reason = reason, description = description).save()

    def save(self, *args, **kwargs):
        super(Stock, self).save(*args, **kwargs)
        StockEvent(stock = self).save()

    def reference(self):
        return "{:05d}".format(self.id)

    def __unicode__(self):
        return "Existencia de {s.product:s} en {s.warehouse:s}".format(s = self)

class StockEvent(models.Model):
    """docstring for StockEvent"""
    stock = models.ForeignKey(Stock)
    date = models.DateTimeField(auto_now_add = True)
    reason = models.CharField(max_length = 500)
    description = models.TextField(blank = True)
    level = models.IntegerField(editable = False, blank = True)

    date.verbose_name = "Fecha"
    reason.verbose_name = "Razón del cambio"
    description.verbose_name = "Descipcion detallada"
    level.verbose_name = "Nueva Cantidad"

    reason.default = "Ajuste administrativo."
    description.default = """\
Ajuste realizado automáticamente o por el administrador, \
generalmente ayuda a corregir las fallas en el inventario, \
o a ingresar el inventario inicial. \
    """

    class Meta():
        """docstring for Meta"""
        ordering = ['stock', '-date']
        get_latest_by = 'date'
        verbose_name = "Evento de inventario"
        verbose_name_plural = "Eventos de inventario"

    def save(self, *args, **kwargs):
        self.level = self.stock.level
        super(StockEvent, self).save(*args, **kwargs)

    def reference(self):
        return "{:05d}".format(self.id)

    def __unicode__(self):
        return "Cambio en el {se.stock:s} por {se.level}".format(se = self)
