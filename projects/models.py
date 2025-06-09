from django.db import models
from cloudinary.models import CloudinaryField

# Create your models here.
class Project(models.Model):
    name = models.CharField(max_length=255, verbose_name="Tên dự án")
    image_file = CloudinaryField(verbose_name="Ảnh dự án (Tải lên từ máy tính)", null=True, blank=True)
    image_url = models.URLField(blank=True, null=True, verbose_name="Ảnh dự án (URL từ Internet)")
    area = models.IntegerField(null=True, blank=True, verbose_name="Diện tích (m²)")
    investor = models.TextField(null=True, blank=True, verbose_name="Chủ đầu tư")
    product = models.TextField(null=True, blank=True, verbose_name="Sản phẩm")
    city = models.CharField(max_length=100, null=True, blank=True, verbose_name="Thành phố")
    created_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.name
    
    @property
    def display_image(self):
        if self.image_file:
            return self.image_file.url
        elif self.image_url:
            return self.image_url
        return None
    
    def save(self, *args, **kwargs):
        if not self.image_file and not self.image_url:
            raise ValueError("Phải cung cấp image_file hoặc image_url.")
        super().save(*args, **kwargs)