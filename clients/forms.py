from django import forms


from clients.models import Client
from clients.models import Payment
from clients.models import Charge

class ClientForm(forms.ModelForm):
    class Meta:
        model = Client

class PaymentForm(forms.ModelForm):
    class Meta:
        model = Payment

class ChargeForm(forms.ModelForm):
    class Meta:
        model = Charge
    