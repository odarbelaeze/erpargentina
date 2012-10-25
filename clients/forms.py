# coding=utf-8
from django import forms
from django.forms import extras

from django.utils import timezone
from django.core.validators import MinValueValidator

from stocks.models import Product

from clients.models import Client
from clients.models import Payment
from clients.models import Charge
from clients.models import PTYPE_CHOICES

from humanresources.models import Worker

class ClientForm(forms.ModelForm):
    error_css_class = "error"
    class Meta:
        model = Client

class PaymentForm(forms.ModelForm):
    error_css_class = "error"
    class Meta:
        model = Payment

class ChargeForm(forms.ModelForm):
    error_css_class = "error"
    class Meta:
        model = Charge

class ClientInfo(forms.Form):
    error_css_class = "error"
    full_name = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(attrs={'class': 'span10', 'placeholder': u'Nombre completo'})
    )
    identification = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(attrs={'class': 'span5', 'placeholder': u'Identificación (opcional)'}),
        required = False
    )
    address = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(attrs={'class': 'span5', 'placeholder': u'Dirección'})
    )
    indication = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(attrs={'class': 'span10', 'placeholder': u'Indicación (opcional)'}),
        required = False
    )
    phone = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(attrs={'class': 'span5', 'placeholder': u'Teléfono'})
    )
    alter_phone = forms.CharField(
        max_length = 100,
        widget = forms.TextInput(attrs={'class': 'span5', 'placeholder': u'Teléfono alternativo (opcional)'}),
        required = False
    )

class ChargeAddForm(forms.Form):
    error_css_class = "error"
    date = forms.DateField(
        widget = extras.SelectDateWidget(attrs={'class': 'span1', 'placeholder': u'Fecha'})
    )
    # vendor = forms.ModelChoiceField(
    #     Worker.objects,
    #     widget = forms.Select(attrs={'class': 'span3', 'placeholder': u'Vendedor'})
    # )
    quantity = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'span1', 'placeholder': u'#'})
    )
    product = forms.ModelChoiceField(
        Product.objects,
        widget = forms.Select(attrs={'class': 'span3', 'placeholder': u'Vendedor'})
    )
    price = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'span1', 'placeholder': u'Precio'}),
        validators = [MinValueValidator(1)]
    )

class PaymentAddForm(forms.Form):
    error_css_class = "error"
    date = forms.DateField(
        widget = extras.SelectDateWidget(attrs={'class': 'span1', 'placeholder': u'Fecha'})
    )
    p_type = forms.ChoiceField(
        choices = PTYPE_CHOICES,
        widget = forms.Select(attrs={'class': 'span3', 'placeholder': u'Tipo'})
    )
    # collector = forms.ModelChoiceField(
    #     Worker.objects,
    #     widget = forms.Select(attrs={'class': 'span3', 'placeholder': u'Cobrador'})
    # )
    amount = forms.IntegerField(
        widget = forms.TextInput(attrs={'class': 'span2', 'placeholder': u'Monto'}),
        validators = [MinValueValidator(1)]
    )

class AddChargeForm(forms.Form):
    error_css_class = "error"
    date = forms.DateTimeField()
    vendor = forms.ModelChoiceField(Worker.objects)
    quantity = forms.IntegerField()
    product = forms.ModelChoiceField(Product.objects)
    price = forms.IntegerField(validators = [MinValueValidator(1)])

    date.label = u'Fecha'
    vendor.label = u'Vendedor'
    quantity.label = u'Cantidad'
    product.label = u'Producto'
    price.label = u'Precio'

class AddPaymentForm(forms.Form):
    error_css_class = "error"
    date = forms.DateTimeField()
    p_type = forms.ChoiceField(choices = PTYPE_CHOICES)
    collector = forms.ModelChoiceField(Worker.objects)
    amount = forms.IntegerField(validators = [MinValueValidator(1)])

    p_type.label = u'Tipo'
    date.label = u'Fecha'
    collector.label = u'Cobrador'
    amount.label = u'Monto'