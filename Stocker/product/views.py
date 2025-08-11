from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.db.models import Q
from product.models import Product
from django.contrib import messages
from main.models import Category, Supplier
from django.core.paginator import Paginator
from .forms  import ProductForm
from django.contrib.auth.models import User
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings
import csv

# Create your views here.

def search_view(request:HttpRequest):
    ''' This Funstion for search product depend on product  or supplier or category name '''
    #used query Q for searching 
    query = request.GET.get("search", "")
    page_obj = []
    categories = Category.objects.all()
    suppliers =  Supplier.objects.all()
    if query:
        page_obj = Product.objects.filter(
        Q(name__icontains=query) |
        Q(category__category_name__icontains=query) |
        Q(suppliers__name__icontains=query)
    ).distinct()
    return render(request, "product/search.html", {"page_obj": page_obj,'categories':categories, 'suppliers':suppliers,})

#-----------------------------------------------------------------------------------
def add_product_view(request : HttpRequest):
    ''' This Fuction for add new product '''
    #check if the user have permisstions for adding 
    if not request.user.has_perm("product.add_product"):
        messages.warning(request, "only employee and manager can add product", "alert-warning")
        return redirect("product:all_product_view")
     #get all the supplier and category to display it in the form while adding 
    categories = Category.objects.all()
    suppliers =  Supplier.objects.all()
    try:
        #add the product to ProductForm
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
    
    return render(request, "product/products.html",{"product_form":product_form,'categories':categories
                                                   ,'suppliers':suppliers})
         

#-----------------------------------------------------------------------------------
def update_product_view(request : HttpRequest, product_id:int):
    ''' This Fuction for update product '''
    #check if the user have permisstions for updating 
    if not request.user.has_perm("product.change_product"):
        messages.warning(request, "only employee and manager can update product", "alert-warning")
        return redirect("product:all_product_view")
    product = Product.objects.get(pk=product_id)
    try:
        #update the product based on user entery 
        product.name = request.POST["name"]
        product.description = request.POST["description"]
        product.quantity = int(request.POST["quantity"])
        product.price = request.POST["price"]
        product.category = Category.objects.get(pk=request.POST["category"])
        product.suppliers.set(request.POST.getlist("suppliers"))
        if "picture" in request.FILES:
                product.picture = request.FILES["picture"]
        product.save()
        messages.success(request, "Product updated successfully", "alert-success")
        #chack if the quantity is less than 5 it will send email for low stock 
        if product.quantity < 5:
            send_email(request)
    except Exception as e:
        messages.error(request, f"Couldn't Update Product {e}", "alert-danger")

    return redirect("product:all_product_view")
    
#-----------------------------------------------------------------------------------
def all_product_view(request : HttpRequest):
    ''' This Fuction for display all products '''
    #take all the product and categories to display in the filter label 
    products = Product.objects.all().order_by("id")
    categories = Category.objects.all()
    suppliers =  Supplier.objects.all()
    product_form = ProductForm()
    selected_category = request.GET.get('category')
    selected_supplier = request.GET.get('suppliers')
    if selected_category and selected_category != 'all':
        products = products.filter(category=selected_category)
    if selected_supplier and selected_supplier != 'all':
        products = products.filter(suppliers=selected_supplier)
    #pagination 
    paginator = Paginator(products, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return render(request, "product/products.html",{'products': products,'product_form':product_form ,
                                                    'categories':categories, 'suppliers':suppliers,
                                  'selected_category':selected_category, 'selected_supplier' :selected_supplier,
                                         'page_obj': page_obj      })

#-----------------------------------------------------------------------------------
def delete_product_view(request : HttpRequest, product_id:int):
    ''' This Fuction for delete product '''
    #check if the user have permisstions for deleting 
    if not request.user.has_perm("product.delete_product"):
        messages.warning(request, "only admin can delete product", "alert-warning")
        return redirect("main:home_view")

    try:
        #delete the product 
        product = Product.objects.get(pk=product_id)
        product.delete()
        messages.success(request, "Deleted Product successfully", "alert-success")
    except Exception as e:
        messages.error(request, "Couldn't Delete Product", "alert-danger")

    return redirect("product:all_product_view")

#-----------------------------------------------------------------------------------
def send_email(request : HttpRequest):
    ''' This Fuction for sending email if there is some low stock products  '''
    # take the low stock products to send it to the admin email 
    low_stock_products = Product.objects.filter(quantity__lt=5, quantity__gt=0)
    content_html = render_to_string("main/mail/alerts.html", {"low_stock_products" :low_stock_products})
    #get the admin email 
    superuser = User.objects.filter(is_superuser=True).first()
    if superuser and superuser.email:
        #send the email 
        send_to = superuser.email
        email_message = EmailMessage("Low Stock Alert", content_html, settings.EMAIL_HOST_USER,[send_to])
        email_message.content_subtype = "html"
        email_message.send()

    messages.warning(request, "You have some low stock product please check your email. Thank You.", "alert-success")

#-----------------------------------------------------------------------------------
def export_view(request : HttpRequest):
    ''' This Fuction for export data to CSV file  '''
    #take all the products with its detail 
    products = Product.objects.all()
    status = ""
    response = HttpResponse(content_type='text/csv')
    response['Content-Disposition'] = 'attachment; filename="products.csv"'
    writer = csv.writer(response)
    writer.writerow(['id', 'name','picture','description' ,'category', 'suppliers','satus','quantity','price'])
    for product in products: 
         #check the quantity to put the status 
         if product.quantity == 0:
             status = "Out of Stock"
         elif product.quantity<5:
             status = "Low Stock"
         else:
             status = "Available"
             #to display the suppliers in each product 
         supplier_names = ", ".join([s.name for s in product.suppliers.all()])
         writer.writerow([product.id, product.name,product.picture.url,product.description, product.category, supplier_names, status, product.quantity, product.price])
    return response