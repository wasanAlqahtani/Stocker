from django.shortcuts import render
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from product.models import Product
# Create your views here.

def search_view(request:HttpRequest):
    query = request.GET.get("search", "")
    action = []
    if query:
        products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__category_name__icontains=query) |
        Q(suppliers__name__icontains=query)
    ).distinct()
    return render(request, "product/search.html", {"products": products})

def add_product_view(request : HttpRequest):
    pass

def update_product_view(request : HttpRequest):
    pass

def product_detail_view(request : HttpRequest):
    pass

def all_product_view(request : HttpRequest):
    return render(request, "product/products.html")
def stock_managment_view(request : HttpRequest):
    pass

def delete_product_view(request : HttpRequest):
    '''admin only'''
    pass


