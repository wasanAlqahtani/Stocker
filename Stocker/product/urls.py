from django.urls import path
from . import views

app_name = "product"

urlpatterns = [
    path("all/", views.all_product_view, name="all_product_view"),
    path("search/",views.search_view,name="search_view"),
    path("add/",views.add_product_view,name="add_product_view"),
    path("export/",views.export_view, name="export_view"),
    path("delete/<int:product_id>/",views.delete_product_view, name="delete_product_view"),
    path("update/<int:product_id>", views.update_product_view, name="update_product_view"),
]