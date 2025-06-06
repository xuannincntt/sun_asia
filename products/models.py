from django.db import models
from tinymce import models as tinymce_models
import cloudinary.uploader
import os
from .utils import create_unique_slug

class Category(models.Model):
    name = models.CharField(max_length=255)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    description = tinymce_models.HTMLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            self.slug = create_unique_slug(self, name_field='name')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255)
    category = models.ForeignKey('Category', on_delete=models.CASCADE, default=5)
    description = tinymce_models.HTMLField(null=True, blank=True)
    sold = models.IntegerField(null=True, default=0, blank=True)
    stock = models.IntegerField(null=True, default=0, blank=True)
    sale_price = models.FloatField(null=True, default=0, blank=True)
    org_price = models.FloatField(null=True, default=0, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            self.slug = create_unique_slug(self, name_field='name')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(upload_to='products/images/', null=True)
    image_url = models.URLField(blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"

