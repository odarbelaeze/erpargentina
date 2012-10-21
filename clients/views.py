# coding=utf-8

from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import redirect
from django.shortcuts import get_object_or_404
from django.shortcuts import render

from django.utils import timezone

from django.forms.models import modelformset_factory
from django.forms.models import formset_factory

from clients.models import Route
from clients.models import Client
from clients.models import Charge
from clients.models import Payment

from clients.forms import ClientForm
from clients.forms import ChargeForm
from clients.forms import PaymentForm
from clients.forms import ChargeAddForm
from clients.forms import PaymentAddForm
from clients.forms import AddPaymentForm
from clients.forms import AddChargeForm
from clients.forms import ClientInfo

class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class RouteList(LoginRequiredMixin, ListView):
    model = Route
    paginate_by = 15

class ClientList(LoginRequiredMixin, ListView):
    model = Client
    paginate_by = 15

class RouteDetail(LoginRequiredMixin, DetailView):
    model = Route

class ClientDetail(LoginRequiredMixin, DetailView):
    model = Client
    def get_context_data(self, **kwargs):
        context = super(ClientDetail, self).get_context_data(**kwargs)
        try:
            context['form_charge'] = AddChargeForm(
                initial = {'date': timezone.now(), 'collector': self.request.user.worker}
            )
        except:
            context['form_charge'] = AddChargeForm(initial = {'date': timezone.now()})
        try:
            context['form_payment'] = AddPaymentForm(
                initial = {'date': timezone.now(), 'collector': self.request.user.worker}
            )
        except:
            context['form_payment'] = AddPaymentForm(initial = {'date': timezone.now()})
        return context

def new_client(request, pk = 1):

    ChargeFormSet = formset_factory(ChargeAddForm, extra = 3)
    PaymentFormSet = formset_factory(PaymentAddForm, extra = 10)

    if request.method == 'POST':
        print "I'll do something cool."
        return redirect('route-detail', pk = pk, permanent = False)
    else:
        client_form = ClientInfo(prefix = 'client')
        charge_formset = ChargeFormSet(prefix = 'charges')
        payment_formset = PaymentFormSet(prefix = 'payments')
        context = {
            'client_form': client_form,
            'charge_formset': charge_formset,
            'payment_formset': payment_formset,
        }
        return render(request, 'clients/client_add.html', context)

def add_charge(request, pk = None):
    client = get_object_or_404(Client, pk = pk)
    if request.method == 'POST':
        form = AddChargeForm(request.POST)
        if form.is_valid():
            data = form.cleaned_data
            client.charge_set.add(Charge(
                date = data['date'],
                vendor = data['vendor'],
                quantity = data['quantity'],
                product = data['product'],
                price = data['price']
            ))
            client.save()

    return redirect('client-detail', pk = pk, permanent = False)

def add_payment(request, pk = None):
    client = get_object_or_404(Client, pk = pk)
    if request.method == 'POST':
        form = AddPaymentForm(request.POST)
        if form.is_valid(): 
            data = form.cleaned_data
            client.payment_set.add(Payment(
                date = data['date'], 
                collector = data['collector'], 
                p_type = data['p_type'],
                amount = data['amount']
            ))
            client.save()

    return redirect('client-detail', pk = pk, permanent = False)