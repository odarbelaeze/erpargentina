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

from django.forms.models import formset_factory

from clients.models import *
from clients.forms import *

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
                initial = {'date': timezone.now(), 'vendor': context['client'].route.in_charge}
            )
        except:
            context['form_charge'] = AddChargeForm(initial = {'date': timezone.now()})
        try:
            context['form_payment'] = AddPaymentForm(
                initial = {'date': timezone.now(), 'collector': context['client'].route.in_charge}
            )
        except:
            context['form_payment'] = AddPaymentForm(initial = {'date': timezone.now()})
        return context

def new_client(request, pk = 1):

    route = get_object_or_404(Route, pk = pk)
    ChargeFormSet = formset_factory(ChargeAddForm, extra = 1)
    PaymentFormSet = formset_factory(PaymentAddForm, extra = 10)

    tz = timezone.get_current_timezone()

    if request.method == 'POST':
        print "I'll do something cool."
        client_form = ClientInfo(request.POST, prefix = 'client')
        charge_formset = ChargeFormSet(request.POST, prefix = 'charges')
        payment_formset = PaymentFormSet(request.POST, prefix = 'payments')

        if (client_form.is_valid() and
         any([form.is_valid() for form in charge_formset]) and
         any([form.is_valid() for form in payment_formset])):
            
            # Create the client

            data = client_form.cleaned_data
            clt = Client(
                route = route,
                full_name = data['full_name'],
                identification = data['identification'],
                address = data['address'],
                indication = data['indication'],
                phone_number = data['phone'],
                alter_phone_number = data['alter_phone']
            )
            clt.save()

            # Add the charges

            for form in charge_formset:
                if form.is_valid() and not form.cleaned_data == {}:
                    data = form.cleaned_data
                    now = timezone.datetime(data['date'].year, data['date'].month, data['date'].day)
                    clt.charge_set.add(Charge(
                        date = timezone.make_aware(now, tz),
                        vendor = route.in_charge,
                        quantity = data['quantity'],
                        product = data['product'],
                        price = data['price']
                    ))

            # Add payments

            for form in payment_formset:
                if form.is_valid():
                    data = form.cleaned_data
                    now = timezone.datetime(data['date'].year, data['date'].month, data['date'].day)
                    clt.payment_set.add(Payment(
                        date = timezone.make_aware(now, tz),
                        collector = route.in_charge,
                        p_type = data['p_type'],
                        amount = data['amount']
                    ))

            # Save the new data

            clt.save()

            return redirect('client-detail', pk = clt.id)

        else:
            context = {
                'client_form': client_form,
                'charge_formset': charge_formset,
                'payment_formset': payment_formset,
                'route_id': pk,
            }
            return render(request, 'clients/client_add.html', context)

        return redirect('route-detail', pk = pk, permanent = False)
    else:
        client_form = ClientInfo(prefix = 'client')
        charge_formset = ChargeFormSet(
            prefix = 'charges', initial = [{
                'date': timezone.now(),
            }])
        payment_formset = PaymentFormSet(
            prefix = 'payments', initial = [{
                'date': timezone.now(),
            }]
        )
        context = {
            'client_form': client_form,
            'charge_formset': charge_formset,
            'payment_formset': payment_formset,
            'route_id': pk,
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