from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from stocks.models import WareHouse
from stocks.models import Product
from stocks.models import PriceTag
from stocks.models import Stock
from stocks.models import StockEvent

class LoginRequiredMixin(object):
    u"""Ensures that user must be authenticated in order to access view."""

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(LoginRequiredMixin, self).dispatch(*args, **kwargs)

class Index(TemplateView):
    template_name = "index.html"
    
class WareHouseList(LoginRequiredMixin, ListView):
    model = WareHouse
    paginate_by = 15

class ProductList(LoginRequiredMixin, ListView):
    model = Product
    paginate_by = 15

class WareHouseDetail(LoginRequiredMixin, DetailView):
    model = WareHouse

class ProductDetail(LoginRequiredMixin, DetailView):
    model = Product
