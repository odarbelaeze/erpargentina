from django.views.generic import TemplateView
from django.views.generic import ListView
from django.views.generic import DetailView

from stocks.models import Product
from stocks.models import PriceTag

class Index(TemplateView):
    """docstring for Index"""
    template_name = "index.html"
        

class ProductList(ListView):
    model = Product