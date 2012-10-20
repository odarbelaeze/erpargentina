from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from django.shortcuts import redirect
from django.shortcuts import render

from django.forms.models import modelformset_factory

from clients.models import Route
from clients.models import Client
from clients.models import Charge
from clients.models import Payment

from clients.forms import ClientForm
from clients.forms import ChargeForm
from clients.forms import PaymentForm

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

def new_client(request, pk = 1):
    print "Aqui estoy"
    PaymentFormSet = modelformset_factory(Payment)
    ChargeFormSet = modelformset_factory(Charge)

    if request.method == 'POST':
        print "I'll do something cool."
        return redirect('route-detail', pk = pk)
    else:
        client_form = ClientForm(prefix = 'client')
        charge_formset = ChargeFormSet(prefix = 'charges')
        payment_formset = PaymentFormSet(prefix = 'payments')
        context = {
            'client_form': client_form,
            'charge_formset': charge_formset,
            'payment_formset': payment_formset,
        }
        return render(request, 'clients/client_add.html', context)


