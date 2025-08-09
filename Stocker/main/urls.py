from django.urls import path
from . import views

app_name = "main"

urlpatterns = [
    path('', views.home_view, name="home_view"),
    path("login/", views.login_view,name="login_view"),
    path("signup/", views.signup_view,name="signup_view"),
    path("categories/", views.all_category_view,name="all_category_view"),
    path("categories/add", views.add_category_view,name="add_category_view"),
    path("categories/delete/<category_id>/", views.delete_category_view,name="delete_category_view"),
    path("categories/update/<int:category_id>/", views.update_category_view,name="update_category_view"),
    path("suppliers/", views.all_supplier_view,name="all_supplier_view"),
    path("suppliers/add", views.add_supplier_view,name="add_supplier_view"),
    path("suppliers/delete/<supplier_id>/", views.delete_supplier_view,name="delete_supplier_view"),
    path("suppliers/update/<supplier_id>/", views.update_supplier_view,name="update_supplier_view"),
    path("signout/", views.sign_out, name="sign_out")
]