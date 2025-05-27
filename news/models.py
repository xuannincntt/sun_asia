from django.db import models

# Create your models here.
class News(models.Model):
    title = models.CharField(max_length=255)
    slug = models.SlugField(unique=True)
    content = models.TextField()
    content_file = models.FileField(upload_to='news/', null=True, blank=True)
    image_url = models.URLField(null=True, blank=True)
    summary = models.TextField(null=True, blank=True)
    published_at = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return self.title