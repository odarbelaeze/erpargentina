from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from clients.models import Route
from clients.models import Client

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