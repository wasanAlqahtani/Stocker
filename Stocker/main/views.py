from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
from django.contrib.auth.models import User
from django.contrib import messages
from main.models import Category, Supplier
from .forms  import CategoryForm, SupplierForm
from django.db import IntegrityError
from django.contrib.auth import authenticate, login, logout
# Create your views here.

def home_view(request : HttpRequest):
     return render(request, "main/home.html")

#-----------------------------------------------------------------------------------
def login_view(request : HttpRequest):
    if request.method == "POST":
        user = authenticate(request, username=request.POST["username"], password=request.POST["password"])
        print(user)
        if user is not None:
            login(request, user)
            messages.success(request, "Logged in successfully", "alert-success")
            return redirect("main:home_view")
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
            return redirect("main:home_view")
        
        except IntegrityError as e:
            messages.error(request, "Please choose another username", "alert-danger")
        except Exception as e:
            messages.error(request, "Couldn't register user. Try again", "alert-danger")
    return render(request, "main/signup.html", {})

#-----------------------------------------------------------------------------------
def sign_out(request: HttpRequest):
    logout(request)
    messages.success(request, "logged out successfully", "alert-warning")
    return redirect(request.GET.get("next", "/"))

#-----------------------------------------------------------------------------------
def add_category_view(request : HttpRequest):
    if not request.user.is_superuser:
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
def category_detail_view(request : HttpRequest, category_id:int):
    pass

#-----------------------------------------------------------------------------------
def update_category_view(request : HttpRequest, category_id:int):
    if not request.user.is_superuser:
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
    if not request.user.is_superuser:
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
    categories = Category.objects.all()
    category_form = CategoryForm()
    return render(request, "main/categories.html",{"categories": categories, "category_form":category_form})

#-----------------------------------------------------------------------------------
def add_supplier_view(request : HttpRequest):
    if not request.user.is_superuser:
        messages.warning(request, "only admin can add supplier", "alert-warning")
        return redirect("main:suppliers.html")
    
#----------------------------------------------------------------------------------
def update_supplier_view(request : HttpRequest, supplier_id:int):
    if not request.user.is_superuser:
        messages.warning(request, "only admin can update supplier", "alert-warning")
        return redirect("main:suppliers.html")
    
#-----------------------------------------------------------------------------------
def all_supplier_view(request : HttpRequest):
    suppliers = Supplier.objects.all()
    return render(request, "main/suppliers.html",{'suppliers': suppliers})

#-----------------------------------------------------------------------------------
def supplier_detail_view(request : HttpRequest, supplier_id:int):
    pass

#-----------------------------------------------------------------------------------
def delete_supplier(request : HttpRequest, supplier_id:int):
    if not request.user.is_superuser:
        messages.warning(request, "only admin can delete supplier", "alert-warning")
        return redirect("main:suppliers.html")
    
    try:
        supplier = Supplier.objects.get(pk=supplier_id)
        supplier.delete()
        messages.success(request, "Deleted Supplier successfully", "alert-success")
    except Exception as e:
        messages.error(request, "Couldn't Delete Supplier", "alert-danger")

    return redirect("main:suppliers.html")



