from django.db import models

class Category(models.Model):
    name = models.CharField(max_length=255)

    def __str__(self):
        return self.name

# Create your models here.
class Product(models.Model):
    category = models.ForeignKey('Category', on_delete=models.CASCADE)
    name = models.CharField(max_length=255)
    desc_file = models.FileField(upload_to='descs/', null=True, blank=True)
    description = models.TextField()
    sale_price = models.FloatField()
    org_price = models.FloatField()
    slug = models.SlugField(max_length=255, unique=True)
    image_main = models.ImageField(upload_to='products/')
    image_sub_1 = models.ImageField(upload_to='products/', null=True, blank=True)
    image_sub_2 = models.ImageField(upload_to='products/', null=True, blank=True)

    def __str__(self):
        return self.name