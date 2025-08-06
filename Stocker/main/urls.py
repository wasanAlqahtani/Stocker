from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path("login/", views.login_view,name="login_view"),
    path("signup/", views.signup_view,name="signup_view"),
    path("categories/", views.all_category_view,name="all_category_view"),
    path("suppliers/", views.all_supplier_view,name="all_supplier_view"),

]