from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views.generic import UpdateView
from django.views.generic import DeleteView

from django.contrib.auth.decorators import login_required
from django.utils.decorators import method_decorator

from stocks.models import WareHouse
from stocks.models import Product
from stocks.models import PriceTag
from stocks.models import Stock
from stocks.models import StockEvent

class Index(TemplateView):
    template_name = "index.html"
    
class WareHouseList(ListView):
    model = WareHouse
    paginate_by = 15

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(WareHouseList, self).dispatch(*args, **kwargs)

class ProductList(ListView):
    model = Product
    paginate_by = 15

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(ProductList, self).dispatch(*args, **kwargs)

class PriceTagList(ListView):
    model = PriceTag
    paginate_by = 15

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(PriceTagList, self).dispatch(*args, **kwargs)


class StockList(ListView):
    model = Stock
    paginate_by = 15

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StockList, self).dispatch(*args, **kwargs)

class StockEventList(ListView):
    model = StockEvent
    paginate_by = 15

    @method_decorator(login_required)
    def dispatch(self, *args, **kwargs):
        return super(StockEventList, self).dispatch(*args, **kwargs)

class WareHouseDetail(DetailView):
    model = WareHouse

class ProductDetail(DetailView):
    model = Product

class PriceTagDetail(DetailView):
    model = PriceTag

class StockDetail(DetailView):
    model = Stock

class StockEventDetail(DetailView):
    model = StockEvent
