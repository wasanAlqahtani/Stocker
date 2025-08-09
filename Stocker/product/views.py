from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from product.models import Product
from django.contrib import messages
from main.models import Category, Supplier
from django.core.paginator import Paginator
from .forms  import ProductForm
from django.core.mail import EmailMessage
from django.conf import settings
# Create your views here.

def search_view(request:HttpRequest):
    query = request.GET.get("search", "")
    products = []
    if query:
        products = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__category_name__icontains=query) |
        Q(suppliers__name__icontains=query)
    ).distinct()
    return render(request, "product/search.html", {"products": products})

#-----------------------------------------------------------------------------------
def add_product_view(request : HttpRequest):
    categories = Category.objects.all()
    suppliers =  Supplier.objects.all()
    try:
        if request.method == "POST":
           product_form = ProductForm(request.POST,request.FILES)
           if product_form.is_valid():
              product_form.save()
              messages.success(request, "Add Product successfully", "alert-success")
              return redirect("product:all_product_view")
        else:
            print("not valid form")
    except Exception as e:
        messages.error(request, "Couldn't Add Product", "alert-danger")
    
    return render(request, "main/categories.html",{"product_form":product_form,'categories':categories
                                                   ,'suppliers':suppliers})
         

#-----------------------------------------------------------------------------------
def update_product_view(request : HttpRequest, product_id:int):
    product = Product.objects.get(pk=product_id)
    try:
        product.name = request.POST["name"]
        product.description = request.POST["description"]
        product.quantity = request.POST["quantity"]
        product.price = request.POST["price"]
        product.category = Category.objects.get(pk=request.POST["category"])
        product.suppliers.set(request.POST.getlist("suppliers"))
        if "picture" in request.FILES:
                product.picture = request.FILES["picture"]
        product.save()
        messages.success(request, "Product updated successfully", "alert-success")
    except Exception as e:
        messages.error(request, "Couldn't Update Product", "alert-danger")

    return redirect("product:all_product_view")
    
#-----------------------------------------------------------------------------------
def all_product_view(request : HttpRequest):
    products = Product.objects.all()
    categories = Category.objects.all()
    suppliers =  Supplier.objects.all()
    product_form = ProductForm()
    selected_category = request.GET.get('category')
    selected_supplier = request.GET.get('suppliers')
    if selected_category and selected_category != 'all':
        products = products.filter(category=selected_category)
    if selected_supplier and selected_supplier != 'all':
        products = products.filter(suppliers=selected_supplier)

    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "product/products.html",{'products': products,'product_form':product_form ,
                                                    'categories':categories, 'suppliers':suppliers,
                                  'selected_category':selected_category, 'selected_supplier' :selected_supplier,
                                         'page_obj': page_obj      })

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

    return redirect("product:all_products_view")

#-----------------------------------------------------------------------------------
def send_low_stock_alert():
    products = Product.objects.all()
    low_stock_products = Product.objects.filter(quantity__lt=5, quantity__gt=0)
