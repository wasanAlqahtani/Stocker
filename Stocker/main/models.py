from django.db import models

# Create your models here.
class Supplier(models.Model):
    name = models.CharField(max_length=1024)
    logo = models.ImageField(upload_to="images/", default="images/default.jpg")
    email = models.EmailField()
    website_link = models.URLField()
    phone_number = models.CharField(max_length=20)
    created_at = models.DateField(auto_now_add=True)

    def __str__(self):
        return self.name

class Category(models.Model):
    category_name = models.CharField(max_length=1024)
    description = models.TextField()
    created_at = models.DateField(auto_now_add=True)
    def __str__(self):
        return self.category_name