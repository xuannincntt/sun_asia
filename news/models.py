from django.db import models
from django.utils.text import slugify
from django.utils import timezone
from tinymce import models as tinymce_models
from cloudinary.models import CloudinaryField

class NewsCategory(models.Model):
    name = models.CharField("Thể loại tin", max_length=100, unique=True)

    def __str__(self):
        return self.name

class News(models.Model):
    title = models.CharField("Tiêu đề", max_length=200)
    published_at = models.DateField("Ngày đăng", default=timezone.now)
    slug = models.SlugField(unique=True, blank=True)
    category = models.ForeignKey(NewsCategory, on_delete=models.CASCADE, verbose_name="Thể loại", default=1)
    content = tinymce_models.HTMLField("Nội dung", null=True, blank=True)
    image_file = CloudinaryField(verbose_name="Ảnh tin tức (Tải lên từ máy tính)", null=True, blank=True)
    views = models.IntegerField("Lượt xem", default=0)
    
    def __str__(self):
        return self.title

    def save(self, *args, **kwargs):
        # Tự động tạo slug nếu chưa có
        if not self.slug:
            self.slug = slugify(self.title)
        super().save(*args, **kwargs)
