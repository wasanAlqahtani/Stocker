from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("all/", views.all_product_view, name="all_product_view"),
]