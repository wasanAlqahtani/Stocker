from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from product.models import Product
from django.contrib import messages
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

#-----------------------------------------------------------------------------------
def add_product_view(request : HttpRequest):
    return redirect("product:all_product_view")

#-----------------------------------------------------------------------------------
def update_product_view(request : HttpRequest):
    pass

#-----------------------------------------------------------------------------------
def product_detail_view(request : HttpRequest, product_id:int):
    product = Product.objects.get(pk=product_id)
    return render(request, 'product/product_detail.html',{"product":product})

#-----------------------------------------------------------------------------------
def all_product_view(request : HttpRequest):
    products = Product.objects.all()
    return render(request, "product/products.html",{'products': products})

#-----------------------------------------------------------------------------------
def stock_managment_view(request : HttpRequest):
    pass

#-----------------------------------------------------------------------------------
def delete_product_view(request : HttpRequest, product_id:int):
    '''admin only'''
    if not request.user.is_superuser:
        messages.warning(request, "only admin can delete product", "alert-warning")
        return redirect("main:home_view")

    try:
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.success(request, "Deleted Product successfully", "alert-success")
    except Exception as e:
        messages.error(request, "Couldn't Delete Product", "alert-danger")

    return redirect("product:products.html")


