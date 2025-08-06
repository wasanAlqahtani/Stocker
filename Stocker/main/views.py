from django.shortcuts import render,redirect
from django.http import HttpRequest, HttpResponse
# Create your views here.

def home_view(request : HttpRequest):
     return render(request, "main/home.html")

def login_view(request : HttpRequest):
    return render(request, "main/login.html")

def signup_view(request : HttpRequest):
    return render(request, "main/signup.html")

def add_category_view(request : HttpRequest):
    pass

def update_category_view(request : HttpRequest):
    pass

def delete_category_view(request : HttpRequest):
    pass

def all_category_view(request : HttpRequest):
    return render(request, "main/categories.html")

def add_supplier_view(request : HttpRequest):
    pass

def update_supplier_view(request : HttpRequest):
    pass

def all_supplier_view(request : HttpRequest):
    return render(request, "main/suppliers.html")

def supplier_detail_view(request : HttpRequest):
    pass

def delete_supplier(request : HttpRequest):
    pass

