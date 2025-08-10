from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import Category, Supplier
from product.models import Product
from .forms  import CategoryForm, SupplierForm
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
from django.db.models import Count
from django.shortcuts import render
import json
# Create your views here.
def home_view(request:HttpRequest):
    return redirect("main:login_view")

def dashboard_view(request : HttpRequest):
     page_obj = Product.objects.order_by('-created_at')[:5]
     categories = Category.objects.all()
     suppliers =  Supplier.objects.all()
     Allproducts = Product.objects.all()

     # Stock status chart 
     labels = ['Out of Stock', 'Low Stock', 'Available']
     counts = [
        Product.objects.filter(quantity=0).count(),
        Product.objects.filter(quantity__gt=0, quantity__lt=5).count(),
        Product.objects.filter(quantity__gte=5).count()
    ]
    # Category Chart 
     categories_counts = (Category.objects.values('category_name').annotate(product_count=Count('product')).order_by('-product_count'))

     category_labels = [item['category_name'] for item in categories_counts]
     category_counts = [item['product_count'] for item in categories_counts]
    
    #Supplier Chart 
     suppliers_counts = Supplier.objects.annotate(product_count=Count('product')).order_by('-product_count')
     supplier_labels = [supplier.name for supplier in suppliers_counts]
     supplier_counts = [supplier.product_count for supplier in suppliers_counts]

     return render(request, "main/dashboards.html",{'Allproducts':Allproducts,'page_obj':page_obj,'categories':categories, 'suppliers':suppliers,
                'labels': json.dumps(labels),'counts': json.dumps(counts),
                'category_labels': json.dumps(category_labels),'category_counts': json.dumps(category_counts),
                 'supplier_labels': json.dumps(supplier_labels), 'supplier_counts': json.dumps(supplier_counts),})

#-----------------------------------------------------------------------------------
def login_view(request : HttpRequest):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect("main:dashboard_view")
        else:
            messages.error(request, "Please try again. You credentials are wrong", "alert-danger")
    return render(request, "main/login.html")

#-----------------------------------------------------------------------------------
def signup_view(request : HttpRequest):
    if request.method == "POST":
        try:
            new_user = User.objects.create_user(username=request.POST["username"],password=request.POST["password"],email=request.POST["email"], first_name=request.POST["first_name"], last_name=request.POST["last_name"])
            new_user.save()
            messages.success(request, "Registered User Successfuly", "alert-success")
            return redirect("main:login_view")
        
        except IntegrityError as e:
            messages.error(request, "Please choose another username", "alert-danger")
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again", "alert-danger")
    return render(request, "main/signup.html", {})

#-----------------------------------------------------------------------------------
def sign_out(request: HttpRequest):
    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")
    return redirect("main:home_view")

#-----------------------------------------------------------------------------------
def add_category_view(request : HttpRequest):
    if not request.user.has_perm("main.add_category"):
        messages.warning(request, "only admin can add category", "alert-warning")
        return redirect("main:all_category_view")
    try:
        if request.method == "POST":
           category_form = CategoryForm(request.POST)
           if category_form.is_valid():
              category_form.save()
              messages.success(request, "Add Category successfully", "alert-success")
              return redirect("main:all_category_view")
        else:
            print("not valid form")
    except Exception as e:
        messages.error(request, "Couldn't Add Category", "alert-danger")
    
    return render(request, "main/categories.html",{"category_form":category_form})
         
     
#-----------------------------------------------------------------------------------
def update_category_view(request : HttpRequest, category_id:int):
    if not request.user.has_perm("main.change_category"):
        messages.warning(request, "only admin can update category", "alert-warning")
        return redirect("main:all_category_view")
    try:
        category = Category.objects.get(pk=category_id)
        category.category_name = request.POST["category_name"]
        category.description = request.POST["description"]
        category.save()
        messages.success(request, "Update Category successfully", "alert-success")
    except Exception as e:
        messages.error(request, "Couldn't Delete Category", "alert-danger")

    return redirect("main:all_category_view")
    
#-----------------------------------------------------------------------------------
def delete_category_view(request : HttpRequest, category_id:int):
    if not request.user.has_perm("main.delete_category"):
        messages.warning(request, "only admin can delete category", "alert-warning")
        return redirect("main:all_category_view")
    
    try:
        category = Category.objects.get(pk=category_id)
        category.delete()
        messages.success(request, "Deleted Category successfully", "alert-success")
    except Exception as e:
        messages.error(request, "Couldn't Delete Category", "alert-danger")

    return redirect("main:all_category_view")

#-----------------------------------------------------------------------------------
def all_category_view(request : HttpRequest):
    categories = Category.objects.all().annotate(total_products=Count('product'))
    category_form = CategoryForm()
    return render(request, "main/categories.html",{"categories": categories, "category_form":category_form})

#-----------------------------------------------------------------------------------
def add_supplier_view(request : HttpRequest):
    if not request.user.has_perm("main.add_supplier"):
        messages.warning(request, "only admin can add supplier", "alert-warning")
        return redirect("main:suppliers.html")
    try:
        if request.method == "POST":
           supplier_form = SupplierForm(request.POST,request.FILES)
           if supplier_form.is_valid():
              supplier_form.save()
              messages.success(request, "Add Supplier successfully", "alert-success")
              return redirect("main:all_supplier_view")
        else:
            print("not valid form")
    except Exception as e:
        messages.error(request, "Couldn't Add Category", "alert-danger")
    
    return render(request, "main/categories.html",{"category_form":supplier_form})
    
#----------------------------------------------------------------------------------
def update_supplier_view(request : HttpRequest, supplier_id:int):
    if not request.user.has_perm("main.change_supplier"):
        messages.warning(request, "only admin can update supplier", "alert-warning")
        return redirect("main:suppliers.html")
    try:
            supplier = Supplier.objects.get(pk=supplier_id)
            supplier.name = request.POST["name"]
            supplier.email = request.POST["email"]
            supplier.website_link = request.POST["website_link"]
            supplier.phone_number = request.POST["phone_number"]
            if "logo" in request.FILES:
                supplier.logo = request.FILES["logo"]
            
            supplier.save()
            messages.success(request, "Supplier updated successfully", "alert-success")
    except Exception as e:
            messages.error(request, "Couldn't update Supplier", "alert-danger")
    
    return redirect("main:all_supplier_view")
    
#-----------------------------------------------------------------------------------
def all_supplier_view(request : HttpRequest):
    suppliers = Supplier.objects.all().annotate(total_products=Count('product'))
    supplier_form = SupplierForm()
    return render(request, "main/suppliers.html",{'suppliers': suppliers, 'supplier_form':supplier_form})

#-----------------------------------------------------------------------------------
def delete_supplier_view(request : HttpRequest, supplier_id:int):
    if not request.user.has_perm("main.delete_supplier"):
        messages.warning(request, "only admin can delete supplier", "alert-warning")
        return redirect("main:all_supplier_view")
    
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
        supplier.delete()
        messages.success(request, "Deleted Supplier successfully", "alert-success")
    except Exception as e:
        messages.error(request, "Couldn't Delete Supplier", "alert-danger")

    return redirect("main:all_supplier_view")

