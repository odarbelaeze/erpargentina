from django.db import models
from django.core.validators import RegexValidator

class Product(models.Model):
    """docstring for Product"""
    reference = models.CharField(max_length = 100, unique = True)
    name = models.CharField(max_length = 255, unique = True)
    description = models.TextField(blank = True)
    stock_level = models.IntegerField(default = 0)

    reference.validators += [RegexValidator(regex = "\A([A-Z]|\d)+\Z")]

    reference.verbose_name = "Referencia"
    name.verbose_name = "Nombre"
    description.verbose_name = "Descipcion"
    stock_level.verbose_name = "Cantidad en Bodega"

    class Meta():
        """docstring for Meta"""
        ordering = ['reference']
        get_latest_by = 'reference'
        verbose_name = "Producto"
        verbose_name_plural = "Productos"

    def has_description(self):
        return bool(self.description)

    def available(self):
        return self.stock_level > 0

    available.boolean = True
    available.short_description = "Producto disponible?"

    def get_price(self):
        pt = self.pricetag_set.latest()
        if pt:
            return pt.price
        else:
            return 0

    get_price.short_description = "Precio actual"

    def __unicode__(self):
        return self.name
    
class PriceTag(models.Model):
    """docstring for PriceTag"""
    date = models.DateTimeField(auto_now_add = True)
    product = models.ForeignKey(Product)
    price = models.PositiveIntegerField()

    class Meta():
        """docstring for Meta"""
        ordering = ['product', '-date']
        get_latest_by = 'date'
        verbose_name = "Precio"
        verbose_name_plural = "Precios"

    def __unicode__(self):
        return "Precio %s" % self.product.name