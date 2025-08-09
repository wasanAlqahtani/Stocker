from django.db import models
from main.models import Category,Supplier

# Create your models here.

class Product(models.Model):
    name = models.CharField(max_length=1024)
    description = models.TextField()
    quantity = models.IntegerField()
    price = models.DecimalField(max_digits=20, decimal_places=2)
    category = models.ForeignKey(Category, on_delete=models.CASCADE)
    suppliers = models.ManyToManyField(Supplier)
    picture = models.ImageField(upload_to="images/", default="images/default.jpg")
    created_at = models.DateField(auto_now_add=True)