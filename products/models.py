from django.db import models
from tinymce.models import HTMLField
import cloudinary.uploader
import os
from .utils import create_unique_slug

class Category(models.Model):
    name = models.CharField(max_length=255,verbose_name="Tên danh mục")
    slug = models.SlugField(max_length=255,unique=True, null=True, blank=True)
    description = HTMLField(null=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            self.slug = create_unique_slug(self, name_field='name')
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name

# Create your models here.
class Product(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên sản phẩm hoặc giải pháp")
    category = models.ForeignKey('Category', verbose_name="Danh mục", on_delete=models.CASCADE, default=5)
    description = HTMLField(verbose_name="Mô tả", null=True, blank=True)
    sold = models.IntegerField(verbose_name="Số lượng đã bán", null=True, default=0, blank=True)
    unit = models.CharField(verbose_name="Đơn vị tính", max_length=255, null=True, default="", blank=True)
    stock = models.IntegerField(verbose_name="Số lượng còn lại",null=True, default=0, blank=True)
    sale_price = models.IntegerField(verbose_name="Giá khuyến mại (Nếu không có thì để trống)", default=-1, null=True, blank=True)
    org_price = models.IntegerField(verbose_name="Giá niêm yết (Nếu không có thì để trống)",null=True, default=-1, blank=True)
    slug = models.SlugField(max_length=255, unique=True, null=True, blank=True)
    created_at = models.DateTimeField(verbose_name="Ngày tạo", auto_now_add=True)
    def save(self, *args, **kwargs):
        if not self.slug or self.slug.strip() == "":
            self.slug = create_unique_slug(self, name_field='name')
        if not self.sale_price:
            self.sale_price = -1
        if not self.org_price:
            self.org_price = -1
        super().save(*args, **kwargs)

    def __str__(self):
        return self.name
    
class ProductImage(models.Model):
    product = models.ForeignKey(Product, on_delete=models.CASCADE, related_name='images')
    image_file = models.ImageField(verbose_name="File ảnh", upload_to='products/images/', null=True)
    image_url = models.URLField(verbose_name="Link ảnh được tạo", blank=True, null=True)
    created_at = models.DateTimeField(verbose_name="Ngày tạo", auto_now_add=True)

    def __str__(self):
        return f"Image for {self.product.name}"

